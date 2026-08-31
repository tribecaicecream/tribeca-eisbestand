from pathlib import Path
import re

path = Path('production.html')
text = path.read_text()
pattern = re.compile(
    r"\$\('#printInventory'\)\.onclick=.*?window\.addEventListener\('afterprint'.*?\);\n",
    re.S,
)
new = r'''function printEsc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function openInventoryPrintPage(){
  if(!latestInventory.matrix.length){alert('Keine Bestandsdaten zum Drucken.');return}
  const w=window.open('','_blank');
  if(!w){alert('Die Druckansicht konnte nicht geöffnet werden. Bitte Pop-ups für diese Seite erlauben.');return}
  const dateInfo=STORES.map(s=>`${s}: ${latestInventory.latest[s]||'–'}`).join(' · ');
  const body=latestInventory.matrix.map(r=>`<tr><td>${printEsc(r.flavor)}</td>${STORES.map(s=>`<td>${r.values[s]>0?fmt(r.values[s]):''}</td>`).join('')}<td class="total-col">${fmt(r.total)}</td></tr>`).join('');
  const totals=`<tr class="sum-row"><td>Gesamt</td>${STORES.map(s=>`<td>${fmt(latestInventory.totals[s])}</td>`).join('')}<td>${fmt(latestInventory.grandTotal)}</td></tr>`;
  w.document.open();
  w.document.write(`<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tribeca Eisbestand</title><style>
    @page{size:A4 portrait;margin:7mm}
    *{box-sizing:border-box;-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
    html,body{margin:0;padding:0;background:#fff;font-family:Arial,Helvetica,sans-serif;color:#101010}
    .sheet{width:100%;margin:0}
    .title{background:#243447;color:#fff;padding:3.2mm 3.5mm 2.8mm;margin:0 0 3mm}
    .title h1{font-size:12pt;line-height:1;margin:0 0 1.2mm;font-weight:700}
    .title .meta{font-size:5.8pt;line-height:1.2;color:#e8eef4}
    table{width:100%;border-collapse:collapse;table-layout:fixed}
    col.flavor{width:38%} col.value{width:12.4%}
    th{background:#c6f3e8;color:#1f2937;font-size:5.8pt;line-height:1.05;font-weight:700;padding:1.5mm 1mm;border-bottom:1.2pt solid #101010;text-align:center;white-space:normal}
    th:first-child{text-align:left}
    td{font-size:6.2pt;line-height:1;padding:1.15mm 1mm;border-bottom:.35pt solid #d9dedc;text-align:center;vertical-align:middle}
    td:first-child{text-align:left;font-weight:600;white-space:nowrap}
    .total-col{font-weight:700;background:#f0f7f5}
    .sum-row td{font-weight:700;background:#dcefe7;border-top:1.2pt solid #101010;border-bottom:0;padding-top:1.4mm;padding-bottom:1.4mm}
    tr{break-inside:avoid;page-break-inside:avoid}
    @media screen{body{padding:12px;background:#eef2f1}.sheet{max-width:210mm;margin:0 auto;background:#fff;box-shadow:0 2px 18px rgba(0,0,0,.12);padding:7mm}}
    @media print{.sheet{padding:0!important;box-shadow:none!important}}
  </style></head><body><div class="sheet"><div class="title"><h1>Tribeca Ice Cream – aktueller Eisbestand</h1><div class="meta">Datenstand: ${printEsc(dateInfo)}</div></div><table><colgroup><col class="flavor">${STORES.map(()=>'<col class="value">').join('')}<col class="value"></colgroup><thead><tr><th>Eissorte</th>${STORES.map(s=>`<th>${printEsc(s)}</th>`).join('')}<th>Gesamt</th></tr></thead><tbody>${body}${totals}</tbody></table></div><script>window.onload=()=>setTimeout(()=>{window.focus();window.print()},250)<\/script></body></html>`);
  w.document.close();
}
$('#printInventory').onclick=openInventoryPrintPage;
'''
updated, count = pattern.subn(new, text, count=1)
if count != 1:
    raise SystemExit(f'print handler pattern matched {count} times')
path.write_text(updated)
