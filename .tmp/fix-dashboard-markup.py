from pathlib import Path
p=Path('production.html')
s=p.read_text(encoding='utf-8')
old='''      </div>\n      </div>\n      <div id="storeBreakdown" class="breakdown"></div>'''
new='''      </div>\n      <div id="storeBreakdown" class="breakdown"></div>'''
if old not in s:
    raise SystemExit('target markup not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
