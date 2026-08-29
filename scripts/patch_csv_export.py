from pathlib import Path
import re

path = Path('production.html')
s = path.read_text(encoding='utf-8')

s = s.replace('id="exportExcel" class="btn" style="width:100%;margin-top:10px;background:transparent">Excel exportieren</button>', 'id="exportExcel" class="btn" style="width:100%;margin-top:10px;background:transparent">CSV exportieren</button>')

pattern = re.compile(r"function xmlEscape\(v\)\{.*?\n\$\('#exportExcel'\)\.onclick=exportAnalyticsExcel;", re.S)
replacement = r'''function csvEscape(v){
  const s=String(v??'');
  return /[;"\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;
}
function csvNumber(v,unit){
  const n=Number(v||0);
  return unit==='EUR'?n.toFixed(2).replace('.',','):String(Math.round(n));
}
function exportAnalyticsCsv(){
  if(!analyticsLoaded)return;
  const key=$('#metricSelect').value,metric=METRICS[key]||METRICS.gross_turnover;
  const rows=analyticsFilter(metricRows,'metric_date');
  const storeFilter=$('#analyticsStore').value;
  const periodLabel=$('#analyticsRange').selectedOptions[0]?.textContent||'';
  const storeLabelText=$('#analyticsStore').selectedOptions[0]?.textContent||'';
  const dates=[...new Set(rows.map(r=>r.metric_date))].sort().reverse();
  const stores=storeFilter==='all'?['Friedrichshain','Prenzlauer Berg','Kreuzberg']:[storeFilter];
  const headers=['Datum','Wochentag',...stores.map(storeLabel),'Gesamt'];
  const lines=[
    'sep=;',
    ['Kennzahl',metric.label].map(csvEscape).join(';'),
    ['Zeitraum',periodLabel].map(csvEscape).join(';'),
    ['Standort',storeLabelText].map(csvEscape).join(';'),
    '',
    headers.map(csvEscape).join(';')
  ];
  dates.forEach(date=>{
    const perStore=stores.map(store=>rows.filter(r=>r.metric_date===date&&r.store===store).reduce((a,r)=>a+metricValue(r,key),0));
    const total=perStore.reduce((a,v)=>a+v,0);
    const weekday=new Date(date+'T12:00:00').toLocaleDateString('de-DE',{weekday:'long'});
    const values=[displayDate(date),weekday,...perStore.map(v=>csvNumber(v,metric.unit)),csvNumber(total,metric.unit)];
    lines.push(values.map(csvEscape).join(';'));
  });
  const csv='\uFEFF'+lines.join('\r\n');
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});
  const url=URL.createObjectURL(blob),a=document.createElement('a');
  const safeMetric=metric.label.replace(/[^a-zA-Z0-9äöüÄÖÜß]+/g,'_').replace(/^_+|_+$/g,'');
  const safePeriod=periodLabel.replace(/[^a-zA-Z0-9äöüÄÖÜß]+/g,'_').replace(/^_+|_+$/g,'');
  a.href=url;a.download=`Tribeca_${safeMetric}_${safePeriod}.csv`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
$('#exportExcel').onclick=exportAnalyticsCsv;'''

if not pattern.search(s):
    raise SystemExit('Existing Excel export function not found')
s = pattern.sub(replacement, s, count=1)
path.write_text(s, encoding='utf-8')
