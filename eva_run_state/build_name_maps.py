import re, json, os, sys, warnings
from pathlib import Path
from multiprocessing import Pool, cpu_count

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

def process_pdf(pdf_path):
    p = Path(pdf_path)
    name = parse_name_from_filename(p.name)
    if not name:
        return None
    try:
        import pdfplumber
        with pdfplumber.open(str(p)) as pdf:
            text = ""
            for page in pdf.pages[:1]:
                t = page.extract_text()
                if t:
                    text += t
        phones = phone_re.findall(text)
        emails = email_re.findall(text)
        return (name, [f"(+86){ph}" for ph in phones], [e.lower() for e in emails])
    except Exception:
        return None

if __name__ == '__main__':
    sorted_dir = Path(r'S:\2 人事\4. 简历库\Sorted')
    unsorted_dir = Path(r'S:\2 人事\4. 简历库\Unsorted')
    all_pdfs = []
    for d in [sorted_dir, unsorted_dir]:
        if d.exists():
            all_pdfs.extend(str(f) for f in d.glob('*.pdf'))

    print(f"Total PDFs: {len(all_pdfs)}", flush=True)

    phone_to_name = {}
    email_to_name = {}
    done = 0

    with Pool(processes=min(8, cpu_count())) as pool:
        for result in pool.imap_unordered(process_pdf, all_pdfs, chunksize=200):
            done += 1
            if result is None:
                continue
            name, phones, emails = result
            for ph in phones:
                phone_to_name[ph] = name
            for em in emails:
                email_to_name[em] = name
            if done % 2000 == 0:
                print(f"  {done}/{len(all_pdfs)} (phone:{len(phone_to_name)} email:{len(email_to_name)})", flush=True)

    print(f"\nDone: {done} PDFs", flush=True)
    print(f"Phone map: {len(phone_to_name)}, Email map: {len(email_to_name)}", flush=True)

    out = Path(r'C:\Users\vecto\Documents\4.VTribe\eva_run_state\name_rescue_maps.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({'phone_to_name': phone_to_name, 'email_to_name': email_to_name}, f, ensure_ascii=False)
    print(f"Saved to {out}", flush=True)
