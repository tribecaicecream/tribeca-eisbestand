from pathlib import Path

path = Path('index.html')
text = path.read_text()

old = """function buildInventoryMatrix(rows,latest){const snapshots={};for(const s of STORES){const d=latest[s];snapshots[s]=new Map(rows.filter(r=>r.store===s&&r.stock_date===d&&FLAVORS.includes(r.flavor)).map(r=>[r.flavor,Number(r.containers)||0]))}const matrix=FLAVORS.map(flavor=>{const values=Object.fromEntries(STORES.map(s=>[s,Number(snapshots[s].get(flavor)||0)]));const total=STORES.reduce((sum,s)=>sum+values[s],0);return{flavor,values,total}}).filter(r=>r.total>0);const totals=Object.fromEntries(STORES.map(s=>[s,matrix.reduce((sum,r)=>sum+r.values[s],0)]));return{matrix,totals,grandTotal:STORES.reduce((sum,s)=>sum+totals[s],0)}}"""
new = """function buildInventoryMatrix(rows,latest){const snapshots={};for(const s of STORES){const d=latest[s];snapshots[s]=new Map(rows.filter(r=>r.store===s&&r.stock_date===d&&FLAVORS.includes(r.flavor)).map(r=>[r.flavor,Number(r.containers)||0]))}const allRows=FLAVORS.map(flavor=>{const values=Object.fromEntries(STORES.map(s=>[s,Number(snapshots[s].get(flavor)||0)]));const total=STORES.reduce((sum,s)=>sum+values[s],0);return{flavor,values,total}});const matrix=[...allRows.filter(r=>r.total>0),...allRows.filter(r=>r.total<=0)];const totals=Object.fromEntries(STORES.map(s=>[s,matrix.reduce((sum,r)=>sum+r.values[s],0)]));return{matrix,totals,grandTotal:STORES.reduce((sum,s)=>sum+totals[s],0)}}"""
if old not in text:
    raise SystemExit('buildInventoryMatrix target not found')
text = text.replace(old,new,1)
text = text.replace('<td class=\"total-col\">${fmt(r.total)}</td>', '<td class=\"total-col\">${qtyCell(r.total)}</td>', 1)
text = text.replace("const dataRows=latestInventory.matrix.map(r=>[r.flavor,...STORES.map(s=>r.values[s]>0?r.values[s]:null),r.total]);", "const dataRows=latestInventory.matrix.map(r=>[r.flavor,...STORES.map(s=>r.values[s]>0?r.values[s]:null),r.total>0?r.total:null]);", 1)
text = text.replace('<td class="total-col">${fmt(r.total)}</td>', '<td class="total-col">${r.total>0?fmt(r.total):\'\'}</td>', 1)
path.write_text(text)
