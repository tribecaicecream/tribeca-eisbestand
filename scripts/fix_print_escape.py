from pathlib import Path
import re

path = Path('index.html')
text = path.read_text()
replacement = '''function printEsc(v){return String(v??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;')}'''
updated, count = re.subn(r"function printEsc\(v\)\{[^\n]+\}", replacement, text, count=1)
if count != 1:
    raise SystemExit(f'printEsc pattern matched {count} times')
path.write_text(updated)
