import json
t=open('template.html').read()
data=open('data.json').read(); paths=open('paths.json').read(); csv=open('published_table_2025_26.csv').read()
esc=lambda s:s.replace('</','<\\/')
out=t.replace('__DATA__',esc(data)).replace('__PATHS__',esc(paths)).replace('__CSV__',esc(json.dumps(csv)))
open('state-poverty-measures.html','w').write(out)
# hosted version: full document
open('index.html','w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+out+'</body></html>')
print(len(out))
