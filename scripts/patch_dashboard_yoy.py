from pathlib import Path

path = Path('production.html')
text = path.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old not in text:
        raise SystemExit(f'Pattern not found: {label}')
    text = text.replace(old, new, 1)


replace_once(
    ".kpi .small{margin-top:7px}\n.breakdown{margin-top:13px;border-top:1px solid var(--line)}\n.breakdown-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:12px}\n.breakdown-row b{text-align:right}",
    ".kpi .small{margin-top:7px}\n.yoy{margin-top:7px;font-size:11px;font-weight:800}\n.yoy.positive{color:var(--green)}.yoy.negative{color:var(--red)}.yoy.neutral{color:var(--muted)}\n.breakdown{margin-top:13px;border-top:1px solid var(--line)}\n.breakdown-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:12px}\n.breakdown-row b{text-align:right}\n.breakdown-value{text-align:right}.breakdown-value .yoy{margin-top:2px;font-size:10px;font-weight:700}",
    'YoY styles',
)

replace_once(
    '<div class="kpi"><small id="selectedMetricLabel">Gross turnover</small><b id="selectedMetricKpi">–</b><div id="selectedMetricMeta" class="small"></div></div>',
    '<div class="kpi"><small id="selectedMetricLabel">Gross turnover</small><b id="selectedMetricKpi">–</b><div id="selectedMetricYoY" class="yoy neutral">Vorjahr: –</div><div id="selectedMetricMeta" class="small"></div></div>',
    'KPI YoY placeholder',
)

replace_once(
    "function fmtEuro(n){return Number(n||0).toLocaleString('de-DE',{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:2})}",
    "function fmtEuro(n){return Number(n||0).toLocaleString('de-DE',{style:'currency',currency:'EUR',minimumFractionDigits:0,maximumFractionDigits:0})}",
    'EUR formatting',
)

replace_once(
    "function metricValue(row,key){return Number((row.metrics&&row.metrics[key])||0)}\nfunction metricFormatter(metric){return metric.unit==='EUR'?fmtEuro:(v=>fmtNumber(v,0))}",
    """function metricValue(row,key){return Number((row.metrics&&row.metrics[key])||0)}
function shiftYearISO(iso,years=-1){
  const [y,m,d]=String(iso).split('-');
  return `${Number(y)+years}-${m}-${d}`;
}
function previousPeriodRows(rows,dateField,currentRows){
  const store=$('#analyticsStore').value;
  const dates=[...new Set(currentRows.map(r=>String(r[dateField]||'')).filter(Boolean))].sort();
  if(!dates.length)return [];
  const start=shiftYearISO(dates[0],-1),end=shiftYearISO(dates[dates.length-1],-1);
  return rows.filter(r=>{
    if(store!=='all'&&r.store!==store)return false;
    const d=String(r[dateField]||'');
    return d>=start&&d<=end;
  });
}
function yoyInfo(current,previous,formatter,hasPrevious){
  if(!hasPrevious)return {text:'Kein Vorjahreswert',cls:'neutral'};
  if(previous===0)return {text:`Vorjahr ${formatter(previous)} · kein %-Vergleich`,cls:'neutral'};
  const pct=Math.round(((current-previous)/previous)*100);
  const sign=pct>0?'+':'';
  return {text:`Vorjahr ${formatter(previous)} · ${sign}${pct} %`,cls:pct>0?'positive':pct<0?'negative':'neutral'};
}
function metricFormatter(metric){return metric.unit==='EUR'?fmtEuro:(v=>fmtNumber(v,0))}""",
    'YoY helper functions',
)

old_render = """function renderAnalytics(){
  if(!analyticsLoaded)return;
  const key=$('#metricSelect').value,metric=METRICS[key]||METRICS.gross_turnover,formatMetric=metricFormatter(metric);
  const selectedRows=analyticsFilter(metricRows,'metric_date');
  const selectedTotal=selectedRows.reduce((a,r)=>a+metricValue(r,key),0);
  const dates=[...new Set(selectedRows.map(r=>r.metric_date))].sort();
  const periodLabel=$('#analyticsRange').selectedOptions[0]?.textContent||'';
  $('#selectedMetricLabel').textContent=metric.label;
  $('#selectedMetricKpi').textContent=formatMetric(selectedTotal);
  $('#selectedMetricMeta').textContent=dates.length?`${periodLabel} · ${dates.length} Berichtstage · ${displayDate(dates[0])} – ${displayDate(dates[dates.length-1])}`:`${periodLabel} · keine Daten`;
  const stores=$('#analyticsStore').value==='all'?['Friedrichshain','Prenzlauer Berg','Kreuzberg']:[$('#analyticsStore').value];
  $('#storeBreakdown').innerHTML=stores.map(store=>{
    const value=selectedRows.filter(x=>x.store===store).reduce((a,x)=>a+metricValue(x,key),0);
    return `<div class="breakdown-row"><span>${storeLabel(store)}</span><b>${formatMetric(value)}</b></div>`;
  }).join('');
  $('#metricChartTitle').textContent=`${metric.label} · einzelne Tage`;
  renderBars('#metricChart',groupByDate(selectedRows,'metric_date',r=>metricValue(r,key)),formatMetric,'sauce');
}"""

new_render = """function renderAnalytics(){
  if(!analyticsLoaded)return;
  const key=$('#metricSelect').value,metric=METRICS[key]||METRICS.gross_turnover,formatMetric=metricFormatter(metric);
  const selectedRows=analyticsFilter(metricRows,'metric_date');
  const previousRows=previousPeriodRows(metricRows,'metric_date',selectedRows);
  const selectedTotal=selectedRows.reduce((a,r)=>a+metricValue(r,key),0);
  const previousTotal=previousRows.reduce((a,r)=>a+metricValue(r,key),0);
  const dates=[...new Set(selectedRows.map(r=>r.metric_date))].sort();
  const periodLabel=$('#analyticsRange').selectedOptions[0]?.textContent||'';
  const totalYoY=yoyInfo(selectedTotal,previousTotal,formatMetric,previousRows.length>0);
  $('#selectedMetricLabel').textContent=metric.label;
  $('#selectedMetricKpi').textContent=formatMetric(selectedTotal);
  $('#selectedMetricYoY').className=`yoy ${totalYoY.cls}`;
  $('#selectedMetricYoY').textContent=totalYoY.text;
  $('#selectedMetricMeta').textContent=dates.length?`${periodLabel} · ${dates.length} Berichtstage · ${displayDate(dates[0])} – ${displayDate(dates[dates.length-1])}`:`${periodLabel} · keine Daten`;
  const stores=$('#analyticsStore').value==='all'?['Friedrichshain','Prenzlauer Berg','Kreuzberg']:[$('#analyticsStore').value];
  $('#storeBreakdown').innerHTML=stores.map(store=>{
    const value=selectedRows.filter(x=>x.store===store).reduce((a,x)=>a+metricValue(x,key),0);
    const previousStoreRows=previousRows.filter(x=>x.store===store);
    const previousValue=previousStoreRows.reduce((a,x)=>a+metricValue(x,key),0);
    const storeYoY=yoyInfo(value,previousValue,formatMetric,previousStoreRows.length>0);
    return `<div class="breakdown-row"><span>${storeLabel(store)}</span><div class="breakdown-value"><b>${formatMetric(value)}</b><div class="yoy ${storeYoY.cls}">${storeYoY.text}</div></div></div>`;
  }).join('');
  $('#metricChartTitle').textContent=`${metric.label} · einzelne Tage`;
  renderBars('#metricChart',groupByDate(selectedRows,'metric_date',r=>metricValue(r,key)),formatMetric,'sauce');
}"""

replace_once(old_render, new_render, 'renderAnalytics')

path.write_text(text, encoding='utf-8')
print('Dashboard YoY patch applied successfully.')
