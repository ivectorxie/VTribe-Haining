import os, re, sys, json
from concurrent.futures import ThreadPoolExecutor
import pymupdf

LOCAL_DIR = r'C:\Users\vecto\Documents\4.VTribe\_pdf_cache'

unmatched_cn = [
    '(+86)12017362265', '(+86)13041038955', '(+86)13114058716',
    '(+86)13167120315', '(+86)13262606215', '(+86)13325681225',
    '(+86)13361276666', '(+86)13527375597', '(+86)13611963990',
    '(+86)13636669606', '(+86)13773103526', '(+86)15052994792',
    '(+86)15321830026', '(+86)15364611519', '(+86)15606279558',
    '(+86)17027633178', '(+86)18550832689', '(+86)18616758586',
    '(+86)18621181138', '(+86)18951129650',
]

search = {p: p[-8:] for p in unmatched_cn}
print(f'Searching for {len(search)} phones by last-8-digits', flush=True)

def scan(filepath):
    filename = os.path.basename(filepath)
    try:
        doc = pymupdf.open(filepath)
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
        hits = {}
        for phone, key in search.items():
            if key in text:
                idx = text.index(key)
                ctx = text[max(0,idx-40):idx+40].replace('\n', '|')
                hits[phone] = ctx
        return filename, hits
    except:
        return filename, {}

files = []
for sub in ['Sorted', 'Unsorted']:
    d = os.path.join(LOCAL_DIR, sub)
    if os.path.isdir(d):
        for f in os.listdir(d):
            files.append(os.path.join(d, f))

print(f'Scanning {len(files)} files...', flush=True)
found_map = {}

with ThreadPoolExecutor(max_workers=20) as ex:
    for i, (fname, hits) in enumerate(ex.map(scan, files)):
        if hits:
            for phone, ctx in hits.items():
                if phone not in found_map:
                    found_map[phone] = []
                found_map[phone].append((fname, ctx))
        if (i+1) % 5000 == 0:
            print(f'  [{i+1}/{len(files)}] found {len(found_map)} phones so far', flush=True)

print(f'\n=== RESULTS ===', flush=True)
for phone in unmatched_cn:
    if phone in found_map:
        print(f'\nFOUND {phone}:', flush=True)
        for fname, ctx in found_map[phone]:
            print(f'  {fname}', flush=True)
            print(f'    ...{ctx}...', flush=True)
    else:
        print(f'NOT FOUND: {phone}', flush=True)
