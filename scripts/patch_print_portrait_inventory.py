from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
start = text.index('@media print{')
end = text.index('\n</style>', start)
new = r'''@media print{
  @page{size:A4 portrait;margin:7mm}
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
  html,body{background:#fff!important;width:100%;height:auto;margin:0!important;padding:0!important}
  body.print-inventory .app{max-width:none!important;padding:0!important;margin:0!important}
  body.print-inventory header,
  body.print-inventory footer,
  body.print-inventory #entry,
  body.print-inventory #history,
  body.print-inventory #dashboard>.card:not(#inventoryCard){display:none!important}
  body.print-inventory #dashboard{display:block!important;margin:0!important;padding:0!important}
  body.print-inventory main{padding:0!important;margin:0!important}
  body.print-inventory #inventoryCard{display:block!important;background:#fff!important;border:0!important;padding:0!important;margin:0!important;break-inside:avoid;page-break-inside:avoid}
  body.print-inventory .inventory-head{display:block!important;margin:0 0 3mm!important;padding:0!important}
  body.print-inventory .inventory-head>div:first-child{background:#243447!important;padding:3mm 3.5mm 2.5mm!important}
  body.print-inventory .inventory-head h3{font-size:12pt!important;line-height:1!important;margin:0 0 1.3mm!important;letter-spacing:.02em!important;color:#fff!important;text-transform:none!important}
  body.print-inventory #inventoryDateInfo{font-size:5.8pt!important;line-height:1.2!important;margin:0!important;color:#e8eef4!important}
  body.print-inventory .inventory-actions{display:none!important}
  body.print-inventory .table-scroll{overflow:visible!important;border-top:0!important}
  body.print-inventory .inventory-matrix{min-width:0!important;width:100%!important;table-layout:fixed!important;border-collapse:collapse!important}
  body.print-inventory .inventory-matrix th:first-child,body.print-inventory .inventory-matrix td:first-child{width:38%!important;white-space:nowrap!important;text-align:left!important}
  body.print-inventory .inventory-matrix th:not(:first-child),body.print-inventory .inventory-matrix td:not(:first-child){width:12.4%!important;text-align:center!important}
  body.print-inventory .inventory-matrix th{background:#c6f3e8!important;color:#1f2937!important;font-size:5.8pt!important;line-height:1.05!important;font-weight:700!important;letter-spacing:.01em!important;text-transform:none!important;padding:1.5mm 1mm!important;border-bottom:1.2pt solid #101010!important;white-space:normal!important}
  body.print-inventory .inventory-matrix td{font-size:6.2pt!important;line-height:1!important;padding:1.15mm 1mm!important;border-bottom:.35pt solid #d9dedc!important;color:#101010!important}
  body.print-inventory .inventory-matrix td:first-child{font-weight:600!important}
  body.print-inventory .inventory-matrix .total-col{font-weight:700!important;background:#f0f7f5!important}
  body.print-inventory .inventory-matrix .matrix-total td{font-weight:700!important;background:#dcefe7!important;border-top:1.2pt solid #101010!important;border-bottom:0!important;padding-top:1.4mm!important;padding-bottom:1.4mm!important}
  body.print-inventory tr{break-inside:avoid!important;page-break-inside:avoid!important}
}'''
text = text[:start] + new + text[end:]
path.write_text(text, encoding='utf-8')
