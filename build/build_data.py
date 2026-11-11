import json,csv
v=json.load(open('/home/claude/published.json'))
ab={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','District of Columbia':'DC','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
fips={'AL':'01','AK':'02','AZ':'04','AR':'05','CA':'06','CO':'08','CT':'09','DE':'10','DC':'11','FL':'12','GA':'13','HI':'15','ID':'16','IL':'17','IN':'18','IA':'19','KS':'20','KY':'21','LA':'22','ME':'23','MD':'24','MA':'25','MI':'26','MN':'27','MS':'28','MO':'29','MT':'30','NE':'31','NV':'32','NH':'33','NJ':'34','NM':'35','NY':'36','NC':'37','ND':'38','OH':'39','OK':'40','OR':'41','PA':'42','RI':'44','SC':'45','SD':'46','TN':'47','TX':'48','UT':'49','VT':'50','VA':'51','WA':'53','WV':'54','WI':'55','WY':'56'}
L={'F':{'FRL':'Meal eligibility (free or reduced-price)','DC':'Direct certification or program participation','INC':'Income, tax or census data','MIX':'Mixed: meal eligibility with another measure','UND':'Poverty factor present, measure not defined in sources read','NONE':'None found in the main formula'},
'A':{'FRL':'Free or reduced-price meal eligibility','PLUS':'Meal eligibility plus other indicators','DC':'Direct certification or program participation, no meal application','OTH':'Other','NF':'Not defined in sources read'},
'M':{'UNI':'Universal free meals law','PART':'Partial or conditional','EXP':'Free meals extended to more students, not universal','NONE':'None found in sources read'},
'C':{'DCI':'Direct certification or identified student percentage','BASE':'Meal data from before CEP carried forward','FORM':'Income form or student-by-student identification','NOMEAL':'Formula does not use meal counts','OTHER':'Other rule, or method not stated','NF':'Not found in sources read'},
'W':{'W1':'Flat weight per student','W2':'Weight or amount that varies with concentration or tier','W3':'Flat dollar amount per student','W4':'Extra staff or instructional time','W5':'Amount not found in sources read','NONE':'No poverty factor found in the main formula'},
'T':{'SB':'Student-based foundation','RB':'Resource-based','GT':'Guaranteed tax base','HY':'Hybrid or other','NF':'Not found in sources read'}}
def S(s): return s.split()
F={};A={};M={};T={}
for k,l in {'FRL':'AZ AR CA CO CT IA KS KY LA ME MN MO NH ND OK UT WA WY','DC':'AL DC IL IN MA MS RI SC TN VA','INC':'NJ NM OR PA VT','MIX':'MD MI NE NY TX','UND':'HI MT NV NC OH','NONE':'AK DE FL GA ID SD WV WI'}.items():
    for s in S(l): F[s]=k
for k,l in {'FRL':'AK AZ AR CO CT DE FL GA HI IN IA KS KY MN MS MT NV NJ ND OK OR RI SD UT WA','PLUS':'CA ID IL LA MI NE NH NY OH TX VA WI VT','DC':'DC MD MA MO NC PA SC TN WV','OTH':'AL','NF':'ME NM WY'}.items():
    for s in S(l): A[s]=k
for k,l in {'UNI':'CA CO MA MI MN NM NY VT','PART':'DC IL ME WA','EXP':'AR DE HI NJ NC ND OH UT'}.items():
    for s in S(l): M[s]=k
for k,l in {'RB':'DE ID NC SD WA WV WY VA','HY':'AL IL ME','GT':'WI VT','NF':'IA'}.items():
    for s in S(l): T[s]=k
C={}
for k,l in {'DCI':'DE GA MI MN MS OK VA','BASE':'AR CA MO WA NE','FORM':'FL IA ME MD NY NC OH PA TX VT WI','NOMEAL':'AL AK DC IL IN MA OR RI SC TN','OTHER':'AZ ID NM'}.items():
    for s_ in S(l): C[s_]=k
unsureC={'GA':'direct certification is used for an appropriation outside the main formula','VA':'two rules: pre-CEP free lunch data for some entitlements, identified student percentage for the at-risk add-on','NE':'greater of the pre-CEP count or a figure built from the identified student percentage','MD':'direct certification and a state income form are both used','CA':'base year carry-forward plus income forms','AK':'the formula has no poverty count at all','FL':'student-level codes; no poverty factor in the main formula','OH':'in FY2026 CEP buildings may code all students as economically disadvantaged','NM':'the row records a CEP participation rule, not a replacement count','AZ':'statute allows an equivalent measure; method not stated','ID':'the definition excludes students eligible only through CEP','MN':'the statute does not call direct certification a CEP substitute','TX':'student-by-student income determination'}
Wm={}
for k,l in {'W1':'AL AZ CA DC HI IA KS KY LA ME MS MO NM ND OK OR PA RI SC TN VT','W2':'AR CO CT IN MA MI MN NE NJ NY OH TX VA','W3':'MD NH','W4':'IL NC WA','W5':'MT NV UT WY','NONE':'AK DE FL GA ID SD WV WI'}.items():
    for s_ in S(l): Wm[s_]=k
unsureW={'CA':'the row records the 0.2 weight only','RI':'the count itself is multiplied by 1.6','IA':'a very small weight on grades 1 to 6 only','NY':'an index built from two counts, each at 0.65','IN':'a concentration index multiplied by a dollar amount','OH':'the row shows 422, a dollar figure scaled by an index','TX':'tiers follow the student\'s neighborhood, not district concentration','CT':'the weight is lower above 60 percent','MA':'dollar increments by twelve groups of district low-income share','MD':'the published cell shows 7842 with no unit','HI':'the measure behind the weight is not defined in sources read','VA':'a fixed add-on plus one that rises with concentration','MN':'weighting factor rises with building concentration','CO':'factor rises with the district share above the state average'}
marker=set(S('DE FL GA ID WI'))
unsure={'AL':'type: Foundation Program plus new weighted allocations, called hybrid','CA':'funding: the count also includes English learners and foster youth','GA':'accountability: plain meal eligibility by my reading','HI':'accountability: nearest match from the plan','IL':'type: evidence-based model, placed under hybrid or other','IN':'accountability: nearest match from the plan','KS':'funding: free meals only, not reduced-price','KY':'funding: free lunch only, not reduced-price','ME':'type: cost model built from staffing, called hybrid','MT':'funding: a payment with no count; type: called student-based','NE':'funding: greater of a tax-based count or free lunch; type: need-minus-resources, called student-based','NC':'accountability: direct certification plus categorical plus a local method','ND':'meals: free meals up to 225 percent of poverty','OH':'funding: measure is as defined by the department','OR':'accountability: also counts all students at schools with free lunch for all','PA':'accountability: several poverty data sources chosen by the district','SD':'accountability: also counts all students at CEP schools','TX':'funding: student count weighted by a census block index','VT':'type: spending per weighted pupil with a statewide tax, called guaranteed tax base','VA':'type: staffing-standards cost, called resource-based','WV':'type: allowances for personnel, called resource-based','WY':'funding: the count also includes English learners and mobile students; type: block grant model, called resource-based','MI':'accountability: the definition read is the at-risk program one','AL ':''}
out=[]; rows=[]
for r in v[1:]:
    r=r+['']*15; a=ab[r[0]]
    f=F[a]; ac=A[a]; m=M.get(a,'NONE'); t=T.get(a,'SB')
    out.append(dict(state=r[0],abbr=a,fips=fips[a],measure=r[1],weight=r[2],acct=r[3],meals=r[4],cep=r[5],type=r[6],base=r[7],st_f=r[8],st_a=r[9],st_m=r[10],st_t=r[11],rows=r[12],notes=r[13],sources=r[14],cF=f,cA=ac,cM=m,cT=t,cC=C.get(a,'NF'),cW=Wm[a],marker=a in marker))
    rows.append([r[0],L['F'][f],'yes' if a in marker else '',L['A'][ac],L['M'][m],L['T'][t],unsure.get(a,'')])
SRC=json.load(open('sources.json'))
for o in out: o['src']=SRC.get(o['state'],{})
json.dump(dict(labels=L,states=out),open('data.json','w'))
json.dump(rows,open('cat_rows.json','w'))
crows=[[L['C'][C.get(ab[r[0]],'NF')],unsureC.get(ab[r[0]],'')] for r in v[1:]]
wrows=[[L['W'][Wm[ab[r[0]]]],unsureW.get(ab[r[0]],'')] for r in v[1:]]
import csv as _c
_c.writer(open('w_rows.csv','w',newline='')).writerows([['how poverty is funded: mechanism category (added 2026-11-10)','mechanism: where Claude was unsure']]+wrows)
w=csv.writer(open('published_table_2025_26.csv','w',newline='')); w.writerow(v[0]); w.writerows(v[1:])
from collections import Counter
for k in 'cF cA cM cT cC cW'.split(): print(k,Counter(o[k] for o in out))

