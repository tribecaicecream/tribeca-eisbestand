from pathlib import Path

path = Path('index.html')
text = path.read_text()

old_matrix = """function buildInventoryMatrix(rows,latest){const snapshots={};for(const s of STORES){const d=latest[s];snapshots[s]=new Map(rows.filter(r=>r.store===s&&r.stock_date===d&&FLAVORS.includes(r.flavor)).map(r=>[r.flavor,Number(r.containers)||0]))}const matrix=FLAVORS.map(flavor=>{const values=Object.fromEntries(STORES.map(s=>[s,Number(snapshots[s].get(flavor)||0)]));const total=STORES.reduce((sum,s)=>sum+values[s],0);return{flavor,values,total}}).filter(r=>r.total>0);const totals=Object.fromEntries(STORES.map(s=>[s,matrix.reduce((sum,r)=>sum+r.values[s],0)]));return{matrix,totals,grandTotal:STORES.reduce((sum,s)=>sum+totals[s],0)}}"""
new_matrix = """function buildInventoryMatrix(rows,latest){const snapshots={};for(const s of STORES){const d=latest[s];snapshots[s]=new Map(rows.filter(r=>r.store===s&&r.stock_date===d&&FLAVORS.includes(r.flavor)).map(r=>[r.flavor,Number(r.containers)||0]))}const matrix=FLAVORS.map(flavor=>{const values=Object.fromEntries(STORES.map(s=>[s,Number(snapshots[s].get(flavor)||0)]));const total=STORES.reduce((sum,s)=>sum+values[s],0);return{flavor,values,total}}).sort((a,b)=>(b.total>0)-(a.total>0)||a.flavor.localeCompare(b.flavor,'de'));const totals=Object.fromEntries(STORES.map(s=>[s,matrix.reduce((sum,r)=>sum+r.values[s],0)]));return{matrix,totals,grandTotal:STORES.reduce((sum,s)=>sum+totals[s],0)}}"""
if old_matrix not in text:
    raise SystemExit('matrix target not found')
text = text.replace(old_matrix, new_matrix, 1)

old_render = """const body=matrix.map(r=>`<tr><td>${r.flavor}</td>${STORES.map(s=>`<td>${qtyCell(r.values[s])}</td>`).join('')}<td class=\"total-col\">${fmt(r.total)}</td></tr>`).join('');"""
new_render = """const body=matrix.map(r=>`<tr${r.total===0?' class=\"empty-stock\"':''}><td>${r.flavor}</td>${STORES.map(s=>`<td>${qtyCell(r.values[s])}</td>`).join('')}<td class=\"total-col\">${r.total>0?fmt(r.total):''}</td></tr>`).join('');"""
if old_render not in text:
    raise SystemExit('render target not found')
text = text.replace(old_render, new_render, 1)

old_excel = """const dataRows=latestInventory.matrix.map(r=>[r.flavor,...STORES.map(s=>r.values[s]>0?r.values[s]:null),r.total]);"""
new_excel = """const dataRows=latestInventory.matrix.map(r=>[r.flavor,...STORES.map(s=>r.values[s]>0?r.values[s]:null),r.total>0?r.total:null]);"""
if old_excel not in text:
    raise SystemExit('excel target not found')
text = text.replace(old_excel, new_excel, 1)

old_print = """const body=latestInventory.matrix.map(r=>`<tr><td>${printEsc(r.flavor)}</td>${STORES.map(s=>`<td>${r.values[s]>0?fmt(r.values[s]):''}</td>`).join('')}<td class=\"total-col\">${fmt(r.total)}</td></tr>`).join('');"""
new_print = """const body=latestInventory.matrix.map(r=>`<tr${r.total===0?' class=\"empty-stock\"':''}><td>${printEsc(r.flavor)}</td>${STORES.map(s=>`<td>${r.values[s]>0?fmt(r.values[s]):''}</td>`).join('')}<td class=\"total-col\">${r.total>0?fmt(r.total):''}</td></tr>`).join('');"""
if old_print not in text:
    raise SystemExit('print target not found')
text = text.replace(old_print, new_print, 1)

old_css = ".inventory-matrix .matrix-total td{font-weight:900;border-top:2px solid var(--ink);background:rgba(198,243,232,.42)}"
new_css = ".inventory-matrix .matrix-total td{font-weight:900;border-top:2px solid var(--ink);background:rgba(198,243,232,.42)}\n.inventory-matrix .empty-stock td{color:var(--muted);background:rgba(255,255,255,.45)}\n.inventory-matrix .empty-stock .total-col{background:rgba(240,247,245,.55)}"
if old_css not in text:
    raise SystemExit('css target not found')
text = text.replace(old_css, new_css, 1)

path.write_text(text)
