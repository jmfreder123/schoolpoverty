import json,re,glob
D='/root/.claude/projects/-home-claude/534a9066-0245-5139-b223-d633aa9d2e45/tool-results/'
def load(n):
    raw=open(D+'mcp-Google_Sheets-get_values-%s.txt'%n).read()
    return json.loads(raw[raw.find('{'):])['values']
head=load('1794417509190'); prov=load('1794417511264')
tabs={'1':load('1794417528429'),'2':load('1794417530874'),'3':load('1794417532682'),'4':load('1794417534420')}
def addr(cell):
    # first address in the cell; a note in brackets after a space is dropped; spaces inside an address are encoded
    c=cell.strip()
    if 'http' not in c or re.search('guess',c,re.I) or 'google.com/search' in c: return ''
    c=c[c.index('http'):].split(' ; ')[0]
    c=re.sub(r'\s+\(.*\)\s*$','',c).strip().rstrip('.,')
    return c.replace(' ','%20')
P={}
for r in prov:
    r=r+['']*5
    if r[0]: 
        P[r[0]]=dict(id=r[0],kind=r[1],title=r[2],issuer=r[3],url=addr(r[4]))
col={'1':dict(cite=7,quote=4,ids=10),'2':dict(cite=6,quote=4,ids=7),'3':dict(cite=4,quote=6,ids=7),'4':dict(cite=8,quote=None,ids=9)}
out={}
for h in head:
    h=h+['']*12
    st,tab,row=h[0],h[1].strip()[:1],str(h[2]).strip()
    if not st or st=='Puerto Rico' or not row.isdigit() or tab not in col: continue
    r=tabs[tab][int(row)-1]+['']*14; c=col[tab]
    assert r[1]==st,(st,tab,row,r[1])
    ids=[i.strip() for i in r[c['ids']].split(';') if i.strip()]
    e=out.setdefault(st,{}).setdefault(tab,dict(cite=[],quote=[],sources=[]))
    if r[c['cite']].strip(): e['cite'].append(r[c['cite']].strip())
    if c['quote'] is not None and r[c['quote']].strip(): e['quote'].append(r[c['quote']].strip())
    for i in ids:
        if i in P and P[i] not in e['sources']: e['sources'].append(P[i])
        elif i not in P: e['sources'].append(dict(id=i,kind='',title='(source row not found)',issuer='',url=''))
json.dump(out,open('sources.json','w'))
n=sum(len(e['sources']) for s in out.values() for e in s.values()); nu=sum(1 for s in out.values() for e in s.values() for x in e['sources'] if x['url'])
print(len(out),'states;',n,'source links listed;',nu,'with an address;', sum(1 for s in out.values() for t,e in s.items() if not e['sources']),'topic lines with no source')
print(json.dumps(out['Arizona']['1'])[:900])
