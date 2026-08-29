from pathlib import Path

path = Path('production.html')
s = path.read_text(encoding='utf-8')

s = s.replace('.bar-row{display:grid;grid-template-columns:62px minmax(0,1fr) 75px;', '.bar-row{display:grid;grid-template-columns:92px minmax(0,1fr) 75px;')
s = s.replace('.bar-row{grid-template-columns:54px minmax(0,1fr) 68px}', '.bar-row{grid-template-columns:84px minmax(0,1fr) 68px}')

old = "function shortDate(iso){const [,m,d]=String(iso).split('-');return `${d}.${m}.`}"
new = "function shortDate(iso){const [,m,d]=String(iso).split('-');const wd=new Date(String(iso)+'T12:00:00').toLocaleDateString('de-DE',{weekday:'short'}).replace('.','');return `${d}.${m}. · ${wd}`}"
assert old in s, 'shortDate function not found'
s = s.replace(old, new, 1)

drinks_anchor = '            <option value="wasser_sprudel">Wasser Sprudel</option>\n          </optgroup>'
drinks_repl = '            <option value="wasser_sprudel">Wasser Sprudel</option>\n            <option value="ipa_bier">IPA Bier</option>\n          </optgroup>'
assert drinks_anchor in s, 'Drinks anchor not found'
s = s.replace(drinks_anchor, drinks_repl, 1)
s = s.replace('            <option value="category_pints">Kategorie: Pints</option>\n            <option value="ipa_bier">IPA Bier</option>', '            <option value="category_pints">Kategorie: Pints</option>', 1)

anchor = '''      <div class="kpi-grid">
        <div class="kpi"><small id="selectedMetricLabel">Gross turnover</small><b id="selectedMetricKpi">–</b><div id="selectedMetricMeta" class="small"></div></div>
      </div>'''
repl = anchor + '''
      <button id="exportExcel" class="btn" style="width:100%;margin-top:10px;background:transparent">Excel exportieren</button>'''
assert anchor in s, 'KPI anchor not found'
s = s.replace(anchor, repl, 1)

js_anchor = "$('#analyticsRange').onchange=renderAnalytics;$('#analyticsStore').onchange=renderAnalytics;$('#metricSelect').onchange=renderAnalytics;"
export_js = r'''function xmlEscape(v){return String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&apos;')}
function exportAnalyticsExcel(){
  if(!analyticsLoaded)return;
  const key=$('#metricSelect').value,metric=METRICS[key]||METRICS.gross_turnover;
  const rows=analyticsFilter(metricRows,'metric_date');
  const storeFilter=$('#analyticsStore').value;
  const periodLabel=$('#analyticsRange').selectedOptions[0]?.textContent||'';
  const storeLabelText=$('#analyticsStore').selectedOptions[0]?.textContent||'';
  const dates=[...new Set(rows.map(r=>r.metric_date))].sort().reverse();
  const stores=storeFilter==='all'?['Friedrichshain','Prenzlauer Berg','Kreuzberg']:[storeFilter];
  const headers=['Datum','Wochentag',...stores.map(storeLabel),'Gesamt'];
  const data=dates.map(date=>{
    const perStore=stores.map(store=>rows.filter(r=>r.metric_date===date&&r.store===store).reduce((a,r)=>a+metricValue(r,key),0));
    const total=perStore.reduce((a,v)=>a+v,0);
    const weekday=new Date(date+'T12:00:00').toLocaleDateString('de-DE',{weekday:'long'});
    return [displayDate(date),weekday,...perStore,total];
  });
  const numberStyle=metric.unit==='EUR'?'Currency':'Integer';
  const titleRows=`<Row><Cell ss:StyleID="Title"><Data ss:Type="String">${xmlEscape(metric.label)}</Data></Cell></Row>`+
    `<Row><Cell><Data ss:Type="String">Zeitraum</Data></Cell><Cell><Data ss:Type="String">${xmlEscape(periodLabel)}</Data></Cell></Row>`+
    `<Row><Cell><Data ss:Type="String">Standort</Data></Cell><Cell><Data ss:Type="String">${xmlEscape(storeLabelText)}</Data></Cell></Row>`+
    `<Row/>`;
  const headerRow='<Row>'+headers.map(h=>`<Cell ss:StyleID="Header"><Data ss:Type="String">${xmlEscape(h)}</Data></Cell>`).join('')+'</Row>';
  const bodyRows=data.map(row=>'<Row>'+row.map((v,i)=>i<2?`<Cell><Data ss:Type="String">${xmlEscape(v)}</Data></Cell>`:`<Cell ss:StyleID="${numberStyle}"><Data ss:Type="Number">${Number(v||0)}</Data></Cell>`).join('')+'</Row>').join('');
  const xml=`<?xml version="1.0"?><?mso-application progid="Excel.Sheet"?>`+
    `<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">`+
    `<Styles><Style ss:ID="Default"><Alignment ss:Vertical="Bottom"/><Font ss:FontName="Arial" ss:Size="10"/></Style><Style ss:ID="Title"><Font ss:FontName="Arial" ss:Size="16" ss:Bold="1"/></Style><Style ss:ID="Header"><Font ss:FontName="Arial" ss:Bold="1"/><Interior ss:Color="#C6F3E8" ss:Pattern="Solid"/></Style><Style ss:ID="Currency"><NumberFormat ss:Format="#,##0.00 [$€-407]"/></Style><Style ss:ID="Integer"><NumberFormat ss:Format="0"/></Style></Styles>`+
    `<Worksheet ss:Name="Auswertung"><Table>${titleRows}${headerRow}${bodyRows}</Table></Worksheet></Workbook>`;
  const blob=new Blob([xml],{type:'application/vnd.ms-excel;charset=utf-8'});
  const url=URL.createObjectURL(blob),a=document.createElement('a');
  const safeMetric=metric.label.replace(/[^a-zA-Z0-9äöüÄÖÜß]+/g,'_').replace(/^_+|_+$/g,'');
  const safePeriod=periodLabel.replace(/[^a-zA-Z0-9äöüÄÖÜß]+/g,'_').replace(/^_+|_+$/g,'');
  a.href=url;a.download=`Tribeca_${safeMetric}_${safePeriod}.xls`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
$('#exportExcel').onclick=exportAnalyticsExcel;'''
assert js_anchor in s, 'analytics event anchor not found'
s = s.replace(js_anchor, js_anchor+'\n'+export_js, 1)

path.write_text(s, encoding='utf-8')
