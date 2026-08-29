from pathlib import Path
import re

path = Path('production.html')
s = path.read_text(encoding='utf-8')

range_block = '''<select id="analyticsRange">
        <option value="year-2026" selected>Gesamt 2026</option>
        <option value="7">Letzte 7 Tage</option>
        <optgroup label="2026">
          <option value="2026-01">Januar 2026</option>
          <option value="2026-02">Februar 2026</option>
          <option value="2026-03">März 2026</option>
          <option value="2026-04">April 2026</option>
          <option value="2026-05">Mai 2026</option>
          <option value="2026-06">Juni 2026</option>
          <option value="2026-07">Juli 2026</option>
          <option value="2026-08">August 2026</option>
          <option value="2026-09">September 2026</option>
          <option value="2026-10">Oktober 2026</option>
          <option value="2026-11">November 2026</option>
          <option value="2026-12">Dezember 2026</option>
        </optgroup>
        <option value="year-2025">Gesamt 2025</option>
        <optgroup label="2025">
          <option value="2025-01">Januar 2025</option>
          <option value="2025-02">Februar 2025</option>
          <option value="2025-03">März 2025</option>
          <option value="2025-04">April 2025</option>
          <option value="2025-05">Mai 2025</option>
          <option value="2025-06">Juni 2025</option>
          <option value="2025-07">Juli 2025</option>
          <option value="2025-08">August 2025</option>
          <option value="2025-09">September 2025</option>
          <option value="2025-10">Oktober 2025</option>
          <option value="2025-11">November 2025</option>
          <option value="2025-12">Dezember 2025</option>
        </optgroup>
      </select>'''

range_pattern = re.compile(r'<select id="analyticsRange">.*?</select>', re.S)
if not range_pattern.search(s):
    raise SystemExit('analyticsRange select not found')
s = range_pattern.sub(lambda m: range_block, s, count=1)

filter_block = '''function analyticsFilter(rows,dateField){
  const store=$('#analyticsStore').value,range=$('#analyticsRange').value,latest=latestMetricDate();
  let sevenStart=null;
  if(range==='7'&&latest){
    const d=new Date(latest+'T12:00:00');d.setDate(d.getDate()-6);sevenStart=localDateISO(d);
  }
  return rows.filter(r=>{
    if(store!=='all'&&r.store!==store)return false;
    const d=String(r[dateField]||'');
    if(range.startsWith('year-'))return d.startsWith(range.slice(5)+'-');
    if(range==='7')return !!latest&&d>=sevenStart&&d<=latest;
    if(/^\\d{4}-\\d{2}$/.test(range))return d.startsWith(range);
    return true;
  });
}'''
filter_pattern = re.compile(r'function analyticsFilter\(rows,dateField\)\{.*?\n\}', re.S)
if not filter_pattern.search(s):
    raise SystemExit('analyticsFilter not found')
s = filter_pattern.sub(lambda m: filter_block, s, count=1)

path.write_text(s, encoding='utf-8')
