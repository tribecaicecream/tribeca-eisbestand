from pathlib import Path

path = Path('index.html')
text = path.read_text()
replacements = [
    ("col.flavor{width:38%} col.value{width:12.4%}", "col.flavor{width:30%} col.value{width:14%}"),
    ("th{background:#c6f3e8;color:#1f2937;font-size:5.8pt;line-height:1.05;font-weight:700;padding:1.5mm 1mm;border-bottom:1.2pt solid #101010;text-align:center;white-space:normal}", "th{background:#c6f3e8;color:#1f2937;font-size:6.1pt;line-height:1.05;font-weight:700;padding:1.5mm .8mm;border-bottom:1.2pt solid #101010;text-align:center;white-space:normal}"),
    ("td{font-size:6.2pt;line-height:1;padding:1.15mm 1mm;border-bottom:.35pt solid #d9dedc;text-align:center;vertical-align:middle}", "td{font-size:7.2pt;line-height:1;padding:1.15mm .8mm;border-bottom:.35pt solid #d9dedc;text-align:center;vertical-align:middle}"),
    ("td:first-child{text-align:left;font-weight:600;white-space:nowrap}", "td:first-child{text-align:left;font-weight:600;white-space:nowrap;font-size:6.1pt}")
]
for old, new in replacements:
    if old not in text:
        raise SystemExit(f'target not found: {old}')
    text = text.replace(old, new, 1)
path.write_text(text)
