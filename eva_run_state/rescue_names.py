"""
Rescue unknown names in B-table using PyMuPDF for fast PDF scanning.
Single-threaded to avoid network drive issues.
"""
import re, sys, warnings, openpyxl
from pathlib import Path
import pymupdf

warnings.filterwarnings("ignore")

NEW_PATTERNS = [
    re.compile(r'【(?P<title>[^_【】]+?)\s*[_\s](?P<city>[^_【】]*?)\s+(?P<salary>[^】]*?)】\s*(?P<name>[^】\d]+?)\s+(?P<exp>\d+年(?:以内|应届生|以上|毕业)?)(?:\s*-\s*Copy)?\.pdf', re.UNICODE),
    re.compile(r'【(?P<title>[^_【】]+?)\s*[_\s](?P<city>[^_【】]*?)】\s*(?P<name>[^】\d]+?)\s+(?P<exp>\d+年(?:以内|应届生|以上|毕业)?)(?:\s*-\s*Copy)?\.pdf', re.UNICODE),
    re.compile(r'(?P<name>[^_]+)_(?P<age>\d+岁|[\d\.]+)_(?P<title>[^_]+)_(?P<city>[^_]+)_.*\.pdf', re.UNICODE),
    re.compile(r'】\s*(?P<name>[^\d】\n]+?)\s+(?:\d+年|应届|\d+岁)(?:.*?)(?:\s*-\s*Copy)?\.pdf', re.UNICODE),
]

def parse_name_from_filename(filename):
    core = re.sub(r'\(\d+\)\.pdf$', '.pdf', filename)
    for pat in NEW_PATTERNS:
        m = pat.search(core)
        if m:
            name = (m.groupdict().get('name') or '').strip()
            if name:
                return name
    return None

phone_re = re.compile(r'1[3-9]\d{9}')
email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def main():
    btable = Path(r'S:\2 人事\4. 简历库\人才登记表20260916-B.xlsx')
    sorted_dir = Path(r'S:\2 人事\4. 简历库\Sorted')
    unsorted_dir = Path(r'S:\2 人事\4. 简历库\Unsorted')

    print("Loading B-table...", flush=True)
    wb = openpyxl.load_workbook(btable)
    ws = wb.active
    headers = [c.value for c in ws[1]]
    name_col = headers.index('候选人') + 1
    phone1_col = headers.index('电话1') + 1
    email_col = headers.index('邮箱') + 1

    # Collect unknown records
    phone_to_rows = {}
    email_to_rows = {}
    unknown_count = 0
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row), start=2):
        name = str(row[name_col - 1].value or '').strip()
        if name in ('未知', 'N/A', ''):
            unknown_count += 1
            phone = str(row[phone1_col - 1].value or '').strip()
            email = str(row[email_col - 1].value or '').strip()
            if phone and phone not in ('N/A', ''):
                phone_to_rows.setdefault(phone, []).append(row_idx)
            if email and email not in ('N/A', ''):
                email_to_rows.setdefault(email.lower(), []).append(row_idx)

    print(f"Unknown: {unknown_count}, phones: {len(phone_to_rows)}, emails: {len(email_to_rows)}", flush=True)

    # Collect PDFs
    all_pdfs = []
    for d in [sorted_dir, unsorted_dir]:
        if d.exists():
            all_pdfs.extend(f for f in d.glob('*.pdf'))
    print(f"PDFs: {len(all_pdfs)}", flush=True)

    # Scan PDFs
    matched = 0
    row_name_map = {}
    remaining_targets = set(phone_to_rows.keys()) | set(email_to_rows.keys())

    for i, pdf_path in enumerate(all_pdfs):
        name = parse_name_from_filename(pdf_path.name)
        if not name:
            continue

        try:
            doc = pymupdf.open(str(pdf_path))
            text = ""
            for page in doc:
                text += page.get_text()
                if len(text) > 3000:
                    break
            doc.close()

            # Check phones
            for ph in phone_re.findall(text):
                key = f"(+86){ph}"
                if key in phone_to_rows:
                    for row_idx in phone_to_rows[key]:
                        if row_idx not in row_name_map:
                            row_name_map[row_idx] = name
                            matched += 1

            # Check emails
            for e in email_re.findall(text):
                key = e.lower()
                if key in email_to_rows:
                    for row_idx in email_to_rows[key]:
                        if row_idx not in row_name_map:
                            row_name_map[row_idx] = name
                            matched += 1
        except Exception:
            pass

        if (i + 1) % 2000 == 0:
            print(f"  {i+1}/{len(all_pdfs)} matched={matched}", flush=True)

        # Early exit if all matched
        if matched >= unknown_count:
            print(f"  All matched at {i+1}!", flush=True)
            break

    print(f"\nDone: matched {matched}/{unknown_count}", flush=True)

    # Update B-table
    for row_idx, name in row_name_map.items():
        ws.cell(row=row_idx, column=name_col).value = name

    wb.save(btable)
    wb.close()
    print(f"Saved. {unknown_count - matched} still unknown.", flush=True)

if __name__ == '__main__':
    main()
