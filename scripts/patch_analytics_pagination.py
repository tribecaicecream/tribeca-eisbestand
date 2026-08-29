from pathlib import Path

path = Path('production.html')
s = path.read_text(encoding='utf-8')
old = """async function loadAnalytics(){
  $('#analyticsStatus').textContent='Lade Umsatzdaten …';$('#analyticsStatus').className='small';$('#analyticsContent').style.display='none';
  try{
    const metricData=await api('daily_orderbird_metrics?select=metric_date,store,metrics&order=metric_date.asc');
    metricRows=Array.isArray(metricData)?metricData:[];
    analyticsLoaded=true;$('#analyticsStatus').textContent='';$('#analyticsContent').style.display='block';renderAnalytics();
  }catch(e){analyticsLoaded=false;$('#analyticsStatus').className='err';$('#analyticsStatus').textContent='Umsatzdaten konnten nicht geladen werden.';console.error(e)}
}"""
new = """async function loadAllMetricRows(){
  const all=[];let offset=0;const pageSize=1000;
  while(true){
    const page=await api(`daily_orderbird_metrics?select=metric_date,store,metrics&order=metric_date.asc,store.asc&limit=${pageSize}&offset=${offset}`);
    if(!Array.isArray(page)||!page.length)break;
    all.push(...page);
    if(page.length<pageSize)break;
    offset+=pageSize;
  }
  return all;
}
async function loadAnalytics(){
  $('#analyticsStatus').textContent='Lade Umsatzdaten …';$('#analyticsStatus').className='small';$('#analyticsContent').style.display='none';
  try{
    const metricData=await loadAllMetricRows();
    metricRows=Array.isArray(metricData)?metricData:[];
    analyticsLoaded=true;$('#analyticsStatus').textContent='';$('#analyticsContent').style.display='block';renderAnalytics();
  }catch(e){analyticsLoaded=false;$('#analyticsStatus').className='err';$('#analyticsStatus').textContent='Umsatzdaten konnten nicht geladen werden.';console.error(e)}
}"""
if old not in s:
    if 'async function loadAllMetricRows()' in s:
        raise SystemExit('already patched')
    raise SystemExit('loadAnalytics block not found')
s=s.replace(old,new,1)
path.write_text(s,encoding='utf-8')
