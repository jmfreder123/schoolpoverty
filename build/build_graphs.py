# Builds graphs.json: Census finance series (from the sheet's draft_funding_levels rows) and the federal events timeline (draft_events_log, draft_provenance).
import json,csv,re
D='/root/.claude/projects/-home-claude/534a9066-0245-5139-b223-d633aa9d2e45/tool-results/'
cen=json.load(open('census_sheet_rows.json'))['sheet']           # sheet rows, Census dataset only (read 2026-11-20)
us=[x for x in csv.DictReader(open('/mnt/user-data/uploads/comps_pdfs/_work/census_state_finance_fy2010_2024.csv')) if x['state']=='United States']
abbr={s['state']:s['abbr'] for s in json.load(open('data.json'))['states']}
Y=list(range(2010,2025))
# Price index: BLS CPI-U, series CUUR0000SA0, monthly values saved by Jack on 2026-11-20 (source D085).
# Fiscal year y is averaged over July of y-1 to June of y (Jack's choice). Every year is restated in fiscal year 2024 dollars.
CPIDIR='/mnt/user-data/uploads/comps_pdfs/_work/cpi/'
CM={}
for f in ('cpi_CUUR0000SA0_2009_2018.json','cpi_CUUR0000SA0_2019_2024.json'):
    d=json.load(open(CPIDIR+f)); assert d['status']=='REQUEST_SUCCEEDED'
    for srs in d['Results']['series']:
        assert srs['seriesID']=='CUUR0000SA0'
        for x in srs['data']:
            if re.match(r'M(0[1-9]|1[0-2])$',x['period']): CM[(int(x['year']),int(x['period'][1:]))]=float(x['value'])
CPI={y:sum(CM[k] for k in [(y-1,m) for m in range(7,13)]+[(y,m) for m in range(1,7)])/12 for y in Y}
FAC={y:CPI[2024]/CPI[y] for y in Y}
def num(s):
    s=str(s).strip()
    return None if s=='' else float(s)
def series(get):
    pp=[];ppr=[];sh={'s':[],'l':[],'f':[]};note=[]
    for y in Y:
        r=get(y)
        if r is None: pp.append(None); ppr.append(None); [sh[k].append(None) for k in sh]; continue
        st,lo,fe,tot,enr=r
        pp.append(round(tot/enr))
        ppr.append(round(tot/enr*FAC[y]))
        parts=[p for p in (st,lo,fe) if p is not None]
        ok=abs(sum(parts)-tot)<=max(2000.0,tot*1e-6)   # parts add to the printed total (rounding in thousands allowed)
        for k,p in (('s',st),('l',lo),('f',fe)):
            sh[k].append(round(100*p/tot,1) if (ok and p is not None) else None)
        if not ok: note.append(y)
    return pp,ppr,sh,note
by={}
for r in cen:
    by[(r[1],int(r[2].replace('FY','')))]=(num(r[3]),num(r[4]),num(r[5]),num(r[6]),num(r[7]))
fin={'y':Y,'st':{}}
for name,ab in abbr.items():
    pp,ppr,sh,note=series(lambda y:by.get((name,y)))
    assert all(v is not None for v in pp),name
    fin['st'][ab]={'pp':pp,'ppr':ppr,'s':sh['s'],'l':sh['l'],'f':sh['f']}
    if note: fin['st'][ab]['gap']=note
U={int(x['fy']):x for x in us if True}
assert len({int(x['fy']) for x in us})==15
pp,ppr,sh,note=series(lambda y:(float(U[y]['state_rev'])*1000,float(U[y]['local'])*1000,float(U[y]['federal'])*1000,float(U[y]['total'])*1000,float(U[y]['enrollment'])))
fin['US']={'pp':pp,'ppr':ppr,'s':sh['s'],'l':sh['l'],'f':sh['f']}
fin['cpi']=[round(CPI[y],3) for y in Y]
print('cpi',fin['cpi'])
print('US real',fin['US']['ppr'],'max real',max(max(v['ppr']) for v in fin['st'].values()),'min real',min(min(v['ppr']) for v in fin['st'].values()))
if note: fin['US']['gap']=note
print('gaps',{k:v.get('gap') for k,v in list(fin['st'].items())+[('US',fin['US'])] if v.get('gap')})
print('no state share',[k for k,v in fin['st'].items() if all(x is None for x in v['s'])])
print('US pp',fin['US']['pp'][0],fin['US']['pp'][-1],'max pp',max(max(v['pp']) for v in fin['st'].values()),'min',min(min(v['pp']) for v in fin['st'].values()))
# events
g=json.loads(json.load(open(D+'toolu_01Y8grooEYYcgSoE99dt4Qhm.json'))[0]['text'])['content']['sheets']
def grid(title):
    sh=[s for s in g if s['properties']['title']==title][0]
    return [[c.get('formattedValue','') for c in row.get('values',[])] for row in sh['data'][0]['rowData']]
ev=[r+['']*9 for r in grid('draft_events_log') if r and r[0].startswith('US-D')]
prov={r[0]:r+['']*10 for r in grid('draft_provenance') if r}
SRC={'US-D1':'D055','US-D2':'D055','US-D3':'D055','US-D4':'D055','US-D5':'D055','US-D6':'D055','US-D7':'D056','US-D8':'D057','US-D9':'D058','US-D10':'D059','US-D11':'D060','US-D12':'D061'}
# Plain one-line labels, written for the page (not source text).
LABEL={'US-D1':'Congress passes the Healthy, Hunger-Free Kids Act',
 'US-D2':'States must directly certify most eligible children for free meals: 80 percent at first, rising to 95',
 'US-D3':'A trial begins: selected districts certify children for free meals through Medicaid, with no application',
 'US-D4':'Schools get an option to serve free meals to all students, with no meal forms',
 'US-D5':'The option starts in 3 states, with 4 more allowed in each of the next two years',
 'US-D6':'The option opens to every eligible district in the country',
 'US-D7':'USDA proposes rules for the free-meals-for-all option',
 'US-D8':'USDA’s final rules for the option take effect',
 'US-D9':'The threshold for the option drops from 40 percent to 25 percent',
 'US-D10':'Every Student Succeeds Act: report cards must show results for economically disadvantaged students',
 'US-D11':'A pandemic law lets USDA waive school meal rules nationwide',
 'US-D12':'Keep Kids Fed Act sets end dates for the pandemic waivers and adds money per meal'}
events=[]
for r in ev:
    eid,_,_,edate,eff,dom,typ,desc,cite=r[:9]
    plot=eff if re.match(r'\d{4}-\d\d-\d\d$',eff) else edate
    assert re.match(r'\d{4}-\d\d-\d\d$',plot),(eid,edate,eff)
    p=prov[SRC[eid]]
    events.append(dict(id=eid,date=plot,basis=('took effect' if plot==eff else 'dated'),event_date=edate,effective=eff,label=LABEL[eid],desc=desc,cite=cite,
        src=dict(id=p[0],title=p[2],issuer=p[3],url=p[4],status=p[9])))
events.sort(key=lambda e:(e['date'],e['id']))
assert len(events)==12
for e in events: print(e['date'],e['basis'],e['id'],e['src']['id'],e['label'][:50])
finsrc=[dict(id=prov[i][0],fy=2010+k,url=prov[i][4],status=prov[i][9]) for k,i in enumerate(['D0%d'%n for n in range(40,55)])]
assert all(('elsec%02d'%(x['fy']-2000)) in x['url'] for x in finsrc),finsrc
cpisrc=dict(id='D085',urls=['https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear=2009&endyear=2018','https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear=2019&endyear=2024'],about=[dict(id='D087',url='https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years',title='BLS data page for the series: its title, base period and monthly values'),dict(id='D086',url='https://www.bls.gov/cpi/factsheets/cpi-series-ids.htm',title='BLS fact sheet: how the series code is built')])
json.dump({'fin':fin,'events':events,'finsrc':finsrc,'cpisrc':cpisrc},open('graphs.json','w'),ensure_ascii=False,separators=(',',':'))
import os;print(os.path.getsize('graphs.json'))
