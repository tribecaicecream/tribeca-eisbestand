from pathlib import Path

path = Path('index.html')
text = path.read_text()

replacements = [
    (
        ".title{background:#243447;color:#fff;padding:3.2mm 3.5mm 2.8mm;margin:0 0 3mm}\n    .title h1{font-size:12pt;line-height:1;margin:0 0 1.2mm;font-weight:700}\n    .title .meta{font-size:5.8pt;line-height:1.2;color:#e8eef4}",
        ".title{background:#243447;color:#fff;padding:2.7mm 3.2mm;margin:0}\n    .title h1{font-size:12.5pt;line-height:1;margin:0;font-weight:700}\n    .meta{font-size:6.7pt;line-height:1.2;color:#5b6573;font-style:italic;padding:1.8mm 3.2mm 1.5mm;background:#fff}\n    .spacer{height:1.6mm}"
    ),
    (
        "col.flavor{width:30%} col.value{width:14%}",
        "col.flavor{width:31.8%} col.pb{width:15.3%} col.kb{width:12.9%} col.fh{width:15.3%} col.prod{width:12.9%} col.total{width:11.8%}"
    ),
    (
        "th{background:#c6f3e8;color:#1f2937;font-size:6.1pt;line-height:1.05;font-weight:700;padding:1.5mm .8mm;border-bottom:1.2pt solid #101010;text-align:center;white-space:normal}",
        "th{background:#c6f3e8;color:#1f2937;font-size:7.2pt;line-height:1.05;font-weight:700;padding:1.35mm .7mm;border-bottom:1.2pt solid #101010;text-align:center;white-space:normal}"
    ),
    (
        "td{font-size:7.2pt;line-height:1;padding:1.15mm .8mm;border-bottom:.35pt solid #d9dedc;text-align:center;vertical-align:middle}",
        "td{font-size:7.5pt;line-height:1;padding:1.03mm .7mm;border-bottom:.35pt solid #d9dedc;text-align:center;vertical-align:middle}"
    ),
    (
        "td:first-child{text-align:left;font-weight:600;white-space:nowrap;font-size:6.1pt}",
        "td:first-child{text-align:left;font-weight:400;white-space:nowrap;font-size:7.1pt}"
    ),
    (
        ".total-col{font-weight:700;background:#f0f7f5}",
        ".total-col{font-weight:700;background:#f0f7f5}"
    ),
    (
        ".sum-row td{font-weight:700;background:#dcefe7;border-top:1.2pt solid #101010;border-bottom:0;padding-top:1.4mm;padding-bottom:1.4mm}",
        ".sum-row td{font-weight:700;background:#dcefe7;border-top:1.2pt solid #101010;border-bottom:0;padding-top:1.15mm;padding-bottom:1.15mm}"
    ),
    (
        "</style></head><body><div class=\"sheet\"><div class=\"title\"><h1>Tribeca Ice Cream – aktueller Eisbestand</h1><div class=\"meta\">Datenstand: ${printEsc(dateInfo)}</div></div><table><colgroup><col class=\"flavor\">${STORES.map(()=>'<col class=\"value\">').join('')}<col class=\"value\"></colgroup>",
        "</style></head><body><div class=\"sheet\"><div class=\"title\"><h1>Tribeca Ice Cream – aktueller Eisbestand</h1></div><div class=\"meta\">Datenstand: ${printEsc(dateInfo)}</div><div class=\"spacer\"></div><table><colgroup><col class=\"flavor\"><col class=\"pb\"><col class=\"kb\"><col class=\"fh\"><col class=\"prod\"><col class=\"total\"></colgroup>"
    ),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f'target not found: {old}')
    text = text.replace(old, new, 1)

path.write_text(text)
