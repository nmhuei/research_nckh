import requests, pathlib, json, concurrent.futures, urllib3, re, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
urllib3.disable_warnings()
p=pathlib.Path('/home/ubuntu/university_research/parts/vn_sources');p.mkdir(exist_ok=True)
base='https://en.naric.edu.vn/vietnam-recognised-bodies'
def fetch(i):
 u=base+f'?page={i}';f=p/f'naric{i}.html'
 if f.exists(): text=f.read_text()
 else:
  for attempt in range(3):
   try:
    r=requests.get(u,verify=False,timeout=30);r.raise_for_status();r.encoding='utf-8';text=r.text;f.write_text(text);break
   except Exception:
    if attempt==2: raise
    time.sleep(1)
 s=BeautifulSoup(text,'html.parser');rows=[]
 for tr in s.select('tbody tr'):
  cols=tr.find_all('td')
  if len(cols)!=6: continue
  a=cols[5].find('a')
  rows.append({'source_row':cols[0].get_text(' ',strip=True),'short_name':cols[1].get_text(' ',strip=True),'name':cols[2].get_text(' ',strip=True),'english_name':cols[3].get_text(' ',strip=True),'address':cols[4].get_text(' ',strip=True),'website':(a.get('href','').strip() if a else ''),'source_url':u})
 return i,rows
allrows=[]
for i,rows in concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch,range(0,38)):
 print('page',i,'rows',len(rows),'range',rows[0]['source_row'] if rows else None,rows[-1]['source_row'] if rows else None,flush=True);allrows+=rows
(p/'naric_all_rows.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2))
rows=[]; excluded=[]; by_key={}
for r in allrows:
 n=r['name'].casefold();u=r['website'];e=r['english_name'].casefold()
 if not any(x in n for x in ['đại học','học viện','nhạc viện']) or any(x in n for x in ['cao đẳng','trung cấp']): excluded.append(r);continue
 if not re.match(r'^https?://',u):
  if '.' in u and ' ' not in u: u='https://'+u
  else: excluded.append(r);continue
 domain=urlparse(u).hostname
 if not domain:excluded.append(r);continue
 domain=domain.lower().removeprefix('www.')
 key=(domain,n)
 if key in by_key:
  prior=by_key[key];prior['source_urls']=list(dict.fromkeys(prior['source_urls']+[r['source_url']]))
  continue
 rec={'name':r['name'],'english_name':r['english_name'],'short_name':r['short_name'],'country':'Viet Nam','country_code':'VN','website':u,'domains':[domain],'source_urls':[r['source_url']],'source_tier':'government_registry','verification_note':'Website transcribed from VN-NARIC recognised-bodies registry; registry contains duplicate and historical records; individual site not yet verified.','institution_type':'academy' if any(x in n for x in ['học viện','nhạc viện']) else 'university','address':r['address'],'registry_row':r['source_row']}
 if any(x in n for x in ['phân hiệu','cơ sở ii','cơ sở 2','phân viện','phân khoa']): rec['institution_type']='branch_campus'
 by_key[key]=rec;rows.append(rec)
(p/'naric_excluded_rows.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2))
(p.parent/'vietnam_naric_raw.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('all',len(allrows),'filtered unique name/domain',len(rows),'excluded',len(excluded))
for r in rows:print(r['name'],'|',r['website'])
