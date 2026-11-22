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
# Sources that must never appear on the public page (Jack, 2026-11-22: "don't make them public"): the Nexis Uni copies he downloaded.
# They are cited in the sheet by source ID with no web address; the files are only in his Obsidian vault. Listed by ID here, and any
# provenance row whose type or address cell says 'not public' or 'Nexis Uni' is caught as well.
PRIVATE={'D089','D090','DC-D014','MS-D013','KY-D013'}
P={}
for r in prov:
    r=r+['']*5
    if r[0]: 
        P[r[0]]=dict(id=r[0],kind=r[1],title=r[2],issuer=r[3],url=addr(r[4]))
        if 'not public' in (r[1]+' '+r[4]).lower() or 'nexis uni' in (r[1]+' '+r[4]).lower(): PRIVATE.add(r[0])
# Link fixes from the link check of 2026-11-20. The sheet's provenance tab (column E) was changed the same day; the rest of this
# file still reads the sheet as it stood on 2026-11-11, so the changed addresses are set here by hand. note is shown after the link.
ARCH='Internet Archive copy from %s; the original address no longer works'
FIX={
 'IL-D001':('https://www.ilga.gov/Documents/legislation/ilcs/documents/010500050K18-8.15.htm',''),
 'IL-D004':('https://www.ilga.gov/Legislation/PublicActs/View/103-0532',''),
 'IL-D005':('https://www.ilga.gov/Documents/legislation/ilcs/documents/010501250K2.3.htm',''),
 'WI-D017':('https://dpi.wi.gov/sfs/statistical/basic-facts/section-f','the file is the link "2025-2026" on this page'),
 'WI-D021':('https://web.archive.org/web/20260218063342/https://dpi.wi.gov/administrators/biweekly-mailing/summary-changes-2025-act-15-2025-27-biennial-budget',ARCH%'February 18, 2026'),
 'CO-D011':('https://web.archive.org/web/20220303132719/http://www.cde.state.co.us/accountability/performanceframeworkcalculationguidebook',ARCH%'March 3, 2022'),
 'NC-D008':('https://web.archive.org/web/20260416161459/https://www.dpi.nc.gov/documents/fbs/allotments/state-allotment-policy-manual-fy-2026pdf/download',ARCH%'April 16, 2026'),
 'SD-D010':('https://web.archive.org/web/20260717020713/https://doe.sd.gov/reportcard/documents/0326-TechManual.pdf',ARCH%'July 17, 2026'),
 'ME-D009':('https://web.archive.org/web/20250206192642/https://www.maine.gov/doe/sites/maine.gov.doe/files/inline-files/ME_Amendment%20_VF_2.23.2024.pdf',ARCH%'February 6, 2025'),
 'WV-D015':('','the address no longer works; the U.S. Department of Education copy of this plan is listed here as WV-D016'),
}
for k,(u,n) in FIX.items():
    P[k]['url']=u
    if n: P[k]['note']=n
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
# Sources taken off a line's list after the 2026-11-11 snapshot (Jack's decisions). The source rows stay in the sheet.
DROP={('Vermont','2'):['VT-D006']}   # never read; address gone; removed from accountability row 65 on 2026-11-20
for (st,tab),ids_ in DROP.items():
    e=out[st][tab]; n=len(e['sources']); e['sources']=[x for x in e['sources'] if x['id'] not in ids_]; assert len(e['sources'])==n-len(ids_)
# Changes made in the sheet on 2026-11-20 after the archived files were read as raw text (accountability rows 66 and 63).
e=out['West Virginia']['2']
e['sources'].append(dict(id='WV-D016',kind='ESSA consolidated state plan (U.S. Department of Education copy, archived)',
    title="West Virginia's Consolidated State Plan under ESSA (resubmitted as final version January 9, 2018), as posted by the U.S. Department of Education",
    issuer='West Virginia Department of Education; file posted by the U.S. Department of Education',
    url='https://web.archive.org/web/20230408160238/https://www2.ed.gov/admins/lead/account/stateplan17/wvconsolidatedstateplanfinal.pdf',
    note=ARCH%'April 8, 2023'))
e['cite']=['West Virginia Consolidated State Plan under ESSA (resubmitted as final version January 9, 2018), p. 48 (Low-Income Student); pp. 10, 11, 14-16 (Economically Disadvantaged named); U.S. Department of Education copy (WV-D016)']
e=out['South Dakota']['2']; a='(fetch read; the tool returned the cell in four pieces, joins unchecked)'; b='(raw file read 2026-11-20; the four quoted pieces run on as one cell, in this order)'
assert sum(q.count(a) for q in e['quote'])==1; e['quote']=[q.replace(a,b) for q in e['quote']]
for s_ in out.values():
    for e in s_.values(): e['sources']=[x for x in e['sources'] if x['id'] not in PRIVATE]
assert not any(x['id'] in PRIVATE for s_ in out.values() for e in s_.values() for x in e['sources'])
json.dump(out,open('sources.json','w'))
n=sum(len(e['sources']) for s in out.values() for e in s.values()); nu=sum(1 for s in out.values() for e in s.values() for x in e['sources'] if x['url'])
print(len(out),'states;',n,'source links listed;',nu,'with an address;', sum(1 for s in out.values() for t,e in s.items() if not e['sources']),'topic lines with no source')
print(json.dumps(out['Arizona']['1'])[:900])
