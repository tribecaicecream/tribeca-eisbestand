from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '''@media print{
  @page{size:landscape;margin:12mm}
  html,body{background:#fff!important}
  body.print-inventory .app{max-width:none;padding:0}
  body.print-inventory header,body.print-inventory footer,body.print-inventory #entry,body.print-inventory #history,body.print-inventory #dashboard>.card:not(#inventoryCard){display:none!important}
  body.print-inventory #dashboard{display:block!important}
  body.print-inventory main{padding:0}
  body.print-inventory #inventoryCard{display:block!important;background:#fff;border:0;padding:0;margin:0}
  body.print-inventory .inventory-actions{display:none!important}
  body.print-inventory .table-scroll{overflow:visible;border-top:1px solid #777}
  body.print-inventory .inventory-matrix{min-width:0;width:100%}
  body.print-inventory th,body.print-inventory td{font-size:9pt;padding:5px 4px;border-color:#bbb}
  body.print-inventory .small{color:#333}
}'''
new = '''@media print{
  @page{size:A4 landscape;margin:6mm}
  html,body{background:#fff!important;width:100%;height:auto}
  body.print-inventory .app{max-width:none;padding:0;margin:0}
  body.print-inventory header,body.print-inventory footer,body.print-inventory #entry,body.print-inventory #history,body.print-inventory #dashboard>.card:not(#inventoryCard){display:none!important}
  body.print-inventory #dashboard{display:block!important}
  body.print-inventory main{padding:0;margin:0}
  body.print-inventory #inventoryCard{display:block!important;background:#fff;border:0;padding:0;margin:0;break-inside:avoid;page-break-inside:avoid}
  body.print-inventory .inventory-head{margin:0 0 3mm;display:block}
  body.print-inventory .inventory-head h3{font-size:11pt;margin:0 0 1mm;letter-spacing:.04em}
  body.print-inventory #inventoryDateInfo{font-size:6.5pt;line-height:1.15;margin:0}
  body.print-inventory .inventory-actions{display:none!important}
  body.print-inventory .table-scroll{overflow:visible;border-top:1px solid #777}
  body.print-inventory .inventory-matrix{min-width:0;width:100%;table-layout:fixed;border-collapse:collapse}
  body.print-inventory .inventory-matrix th:first-child,body.print-inventory .inventory-matrix td:first-child{width:29%;white-space:nowrap}
  body.print-inventory .inventory-matrix th:not(:first-child),body.print-inventory .inventory-matrix td:not(:first-child){width:14.2%}
  body.print-inventory th,body.print-inventory td{font-size:6.8pt;line-height:1;padding:1.25mm 1.2mm;border-color:#bbb}
  body.print-inventory th{font-size:6pt;letter-spacing:.05em}
  body.print-inventory tr{break-inside:avoid;page-break-inside:avoid}
  body.print-inventory .small{color:#333}
}'''
if old not in text:
    raise SystemExit('Print CSS block not found; no changes made.')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
print('Updated inventory print CSS for one-page A4 landscape output.')
