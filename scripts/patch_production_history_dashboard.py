from pathlib import Path

path = Path('production.html')
s = path.read_text(encoding='utf-8')

# Add tab.
old_tabs = '''    <button class="tab" data-tab="dashboard">Dashboard</button>\n    <button class="tab" data-tab="history">Historie</button>'''
new_tabs = '''    <button class="tab" data-tab="dashboard">Dashboard</button>\n    <button class="tab" data-tab="productionHistory">Historie Produktion</button>\n    <button class="tab" data-tab="history">Historie</button>'''
if old_tabs not in s and 'data-tab="productionHistory"' not in s:
    raise SystemExit('tab anchor not found')
if 'data-tab="productionHistory"' not in s:
    s = s.replace(old_tabs, new_tabs, 1)

# Add panel before the existing flavor history panel.
history_anchor = '''<section id="history" class="panel">\n  <div class="toolbar"><select id="histFlavor"></select></div>\n  <div class="card"><h3 style="margin-top:0">Historie</h3><div id="historyList"></div></div>\n</section>'''
prod_panel = '''<section id="productionHistory" class="panel">\n  <div class="card">\n    <h3 style="margin-top:0">Historie Produktion</h3>\n    <div class="analysis-controls">\n      <select id="prodHistRange">\n        <option value="all" selected>Gesamter Zeitraum</option>\n        <option value="year-2026">Gesamt 2026</option>\n        <option value="year-2025">Gesamt 2025</option>\n        <option value="7">Letzte 7 Tage</option>\n        <option value="30">Letzte 30 Tage</option>\n      </select>\n      <select id="prodHistFlavor"><option value="all">Alle Sorten</option></select>\n    </div>\n    <div id="prodHistStatus" class="small">Lade Produktionshistorie …</div>\n    <div id="prodHistContent" style="display:none">\n      <div class="summary">\n        <div class="metric"><small>Behälter</small><b id="prodHistContainers">0</b></div>\n        <div class="metric"><small>kg</small><b id="prodHistKg">0,0</b></div>\n        <div class="metric"><small>Produktionstage</small><b id="prodHistDays">0</b></div>\n      </div>\n      <div class="kpi"><small>Ø pro Produktionstag</small><b id="prodHistAverage">0</b><div class="small">Behälter pro erfasstem Produktionstag</div></div>\n      <div class="chart-title" id="prodHistChartTitle">Produktion · einzelne Tage</div>\n      <div id="prodHistChart" class="bar-chart"></div>\n      <div class="chart-title">Sorten im gewählten Zeitraum</div>\n      <div id="prodHistFlavorBreakdown" class="breakdown"></div>\n    </div>\n  </div>\n</section>\n\n'''
if 'id="productionHistory"' not in s:
    if history_anchor not in s:
        raise SystemExit('history panel anchor not found')
    s = s.replace(history_anchor, prod_panel + history_anchor, 1)

# Add production history functions before existing history() function.
func_anchor = '''async function history(){\n  try{'''
prod_functions = r'''let productionHistoryRows=[],productionHistoryLoaded=false;
function fmtProdQty(n){return Number(n||0).toLocaleString('de-DE',{minimumFractionDigits:Number(n)%1?1:0,maximumFractionDigits:1})}
function productionHistoryFilter(rows){
  const range=$('#prodHistRange').value,flavor=$('#prodHistFlavor').value;
  const dates=rows.map(r=>r.production_date).filter(Boolean).sort();
  const latest=dates.length?dates[dates.length-1]:null;
  let start=null;
  if((range==='7'||range==='30')&&latest){
    const d=new Date(latest+'T12:00:00');d.setDate(d.getDate()-(Number(range)-1));start=localDateISO(d);
  }
  return rows.filter(r=>{
    if(flavor!=='all'&&r.flavor!==flavor)return false;
    const d=String(r.production_date||'');
    if(range.startsWith('year-'))return d.startsWith(range.slice(5)+'-');
    if((range==='7'||range==='30'))return !!latest&&d>=start&&d<=latest;
    return true;
  });
}
function renderProductionHistory(){
  if(!productionHistoryLoaded)return;
  const rows=productionHistoryFilter(productionHistoryRows);
  const total=rows.reduce((a,r)=>a+Number(r.containers||0),0);
  const days=[...new Set(rows.map(r=>r.production_date))].sort();
  $('#prodHistContainers').textContent=fmtProdQty(total);
  $('#prodHistKg').textContent=fmtKg(total*KG);
  $('#prodHistDays').textContent=fmtQty(days.length);
  $('#prodHistAverage').textContent=days.length?fmtProdQty(total/days.length):'0';
  const flavor=$('#prodHistFlavor').value;
  $('#prodHistChartTitle').textContent=(flavor==='all'?'Gesamtproduktion':flavor)+' · einzelne Tage';
  const daily=groupByDate(rows,'production_date',r=>Number(r.containers||0));
  renderBars('#prodHistChart',daily,v=>fmtProdQty(v)+' Beh.','sauce');
  const byFlavor={};
  rows.forEach(r=>{byFlavor[r.flavor]=(byFlavor[r.flavor]||0)+Number(r.containers||0)});
  const sorted=Object.entries(byFlavor).sort((a,b)=>b[1]-a[1]);
  $('#prodHistFlavorBreakdown').innerHTML=sorted.length?sorted.map(([name,value])=>`<div class="breakdown-row"><span>${name}</span><b>${fmtProdQty(value)} Beh. · ${fmtKg(value*KG)} kg</b></div>`).join(''):'<div class="small">Keine Produktionsdaten im gewählten Zeitraum.</div>';
}
async function loadProductionHistory(){
  $('#prodHistStatus').textContent='Lade Produktionshistorie …';$('#prodHistStatus').className='small';$('#prodHistContent').style.display='none';
  try{
    const rows=await api('production_entries?flavor=neq.__PRODUCTION_COMPLETE__&containers=gt.0&select=production_date,flavor,containers&order=production_date.asc&limit=5000');
    productionHistoryRows=Array.isArray(rows)?rows:[];
    const select=$('#prodHistFlavor'),current=select.value;
    const flavors=[...new Set(productionHistoryRows.map(r=>r.flavor).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'de'));
    select.innerHTML='<option value="all">Alle Sorten</option>'+flavors.map(f=>`<option value="${f.replace(/&/g,'&amp;').replace(/"/g,'&quot;')}">${f}</option>`).join('');
    if(flavors.includes(current))select.value=current;
    productionHistoryLoaded=true;$('#prodHistStatus').textContent='';$('#prodHistContent').style.display='block';renderProductionHistory();
  }catch(e){productionHistoryLoaded=false;$('#prodHistStatus').className='err';$('#prodHistStatus').textContent='Produktionshistorie konnte nicht geladen werden.';console.error(e)}
}
$('#prodHistRange').onchange=renderProductionHistory;$('#prodHistFlavor').onchange=renderProductionHistory;

'''
if 'async function loadProductionHistory()' not in s:
    if func_anchor not in s:
        raise SystemExit('history function anchor not found')
    s = s.replace(func_anchor, prod_functions + func_anchor, 1)

# Wire tab click.
old_handler = "  if(b.dataset.tab==='dashboard')dashboard();\n  if(b.dataset.tab==='history')history();"
new_handler = "  if(b.dataset.tab==='dashboard')dashboard();\n  if(b.dataset.tab==='productionHistory')loadProductionHistory();\n  if(b.dataset.tab==='history')history();"
if "b.dataset.tab==='productionHistory'" not in s:
    if old_handler not in s:
        raise SystemExit('tab handler anchor not found')
    s = s.replace(old_handler, new_handler, 1)

path.write_text(s, encoding='utf-8')
