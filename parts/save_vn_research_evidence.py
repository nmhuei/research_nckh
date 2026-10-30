import json,pathlib,requests,concurrent.futures,hashlib
from bs4 import BeautifulSoup
p=pathlib.Path('/home/ubuntu/university_research/parts');e=p/'vn_sources'/'research';e.mkdir(exist_ok=True)
data=json.loads((p/'vn_research.json').read_text());urls=set()
for s in data['schools']:
 for r in s['items']:
  urls.add(r['url']);urls.update(r.get('source_urls',[]))
def fetch(u):
 key=hashlib.sha256(u.encode()).hexdigest()[:16];entry={'url':u,'retrieved_at':'2026-10-30'}
 try:
  r=requests.get(u,timeout=25);entry.update({'http_status':r.status_code,'final_url':r.url,'sha256':hashlib.sha256(r.content).hexdigest()})
  if r.ok:
   ext='.pdf' if 'pdf' in r.headers.get('content-type','') else '.html';f=e/(key+ext);f.write_bytes(r.content);entry['file']=str(f)
   if ext=='.html':
    soup=BeautifulSoup(r.content,'html.parser');(e/(key+'.txt')).write_text(soup.get_text('\n',strip=True))
 except Exception as x:entry['error']=str(x)
 return entry
manifest=list(concurrent.futures.ThreadPoolExecutor(6).map(fetch,sorted(urls)));(e/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print('sources',len(manifest),'saved',sum('file'in x for x in manifest));print([{k:x[k] for k in ['url','http_status','error'] if k in x} for x in manifest if 'file'not in x])
# Artifact schema and completeness checks, not product tests.
r=json.loads((p/'vietnam.json').read_text()); required=['name','country','country_code','website','domains','source_urls','source_tier','verification_note']
assert len(r)==265
assert all(all(k in x for k in required) for x in r)
assert len({x['domains'][0] for x in r})==len(r)
example_domains=['usth.edu.vn','hust.edu.vn','uet.vnu.edu.vn','hcmut.edu.vn','uit.edu.vn','ptit.edu.vn','dut.udn.vn','vku.udn.vn','hcmute.edu.vn','vlute.edu.vn','mta.edu.vn','actvn.edu.vn','utc.edu.vn','humg.edu.vn','huce.edu.vn','daihoc.fpt.edu.vn','phenikaa-uni.edu.vn']
assert all(d in {y for x in r for y in x['domains']} for d in example_domains)
assert len(data['schools'])==8 and all(len(s['items'])>=2 for s in data['schools'])
assert sum(len(s['items']) for s in data['schools'])==17
assert all(i['title'] and i['url'].startswith('https://') and i['year']<=2026 and i['type'] and i['topics'] and i['verification_note'] for s in data['schools'] for i in s['items'])
print('PASS: directory fields, unique canonical domains,17 example schools,8 research schools,17 sourced items.')
