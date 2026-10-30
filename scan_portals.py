"""One-time bounded public-page survey; outputs leads, not verified papers."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'.deps'))
import requests,json,re,time,concurrent.futures,ipaddress
from urllib.parse import urlsplit,urljoin,urldefrag
from bs4 import BeautifulSoup
from config import ROOT,DATE,plain,classify

KEYS = ['research','publication','repository','nghien cuu','cong bo','khoa hoc','forschung','publikationen','recherche','publications','ricerca','investigacion','onderzoek','forskning','tutkimus','badania','nauka','vyzkum']
BAD = ['login','sign in','dang nhap','tuyen sinh','admission','career','job','privacy','cookie','donate','contact','register','apply','calendar','event']
def safe(u):
 try:
  p=urlsplit(u); h=p.hostname or ''
  if p.scheme not in ['http','https'] or not h or p.username:return False
  if h=='localhost' or h.endswith(('.local','.internal')):return False
  try:return ipaddress.ip_address(h).is_global
  except ValueError:return '.' in h
 except ValueError:return False
def fetch(s,u):
 start=time.monotonic();out={'url':u,'checked_at':DATE}
 try:
  if not safe(u):raise ValueError('not_public_http_url')
  with s.get(u,timeout=(4,8),stream=True,allow_redirects=True) as r:
   out.update(http_status=r.status_code,final_url=r.url)
   if not r.ok:return out,[]
   if 'html' not in r.headers.get('Content-Type','').lower():return dict(out,note='not_html'),[]
   chunks=[];size=0
   for c in r.iter_content(32768):
    chunks.append(c);size+=len(c)
    if size>=650000 or time.monotonic()-start>13:break
   html=b''.join(chunks)
   soup=BeautifulSoup(html,'html.parser')
   out['title']=soup.title.get_text(' ',strip=True)[:260] if soup.title else ''
   out['h1']=[x.get_text(' ',strip=True)[:220] for x in soup.find_all('h1')[:3]]
   links=[]
   for a in soup.select('a[href]'):
    text=a.get_text(' ',strip=True);href=urldefrag(urljoin(r.url,a['href']))[0]
    if safe(href):links.append((text,href))
   out['outgoing_link_count']=len(links)
   return out,links
 except Exception as e:
  out['error']=type(e).__name__+': '+str(e)[:180];return out,[]

def scan(row):
 s=requests.Session();s.max_redirects=5;s.headers['User-Agent']='UniversityResearchDirectorySurvey/1.0'
 initial=row['website'];https=re.sub('^http:','https:',initial)
 result={'record_id':row['record_id'],'name':row['name'],'country_code':row['country_code'],'website':initial,'technology_selection_basis':row['technology_selection_basis'],'pages':[],'research_portal_leads':[],'research_item_leads':[],'scan_kind':'bounded_automated_discovery_not_deep_review','checked_at':DATE}
 page,links=fetch(s,https);result['pages'].append(page)
 if not links and initial!=https:
  page,links=fetch(s,initial);result['pages'].append(page)
 root_host=(urlsplit(page.get('final_url',initial)).hostname or '').removeprefix('www.')
 allowed=set(row['domains']+[root_host])
 def within(url):
  h=(urlsplit(url).hostname or '').removeprefix('www.')
  return any(h==d or h.endswith('.'+d) for d in allowed if d)
 portals=[]
 for text,url in links:
  content=plain(text+' '+url)
  if within(url) and any(k in content for k in KEYS) and not any(k in plain(text) for k in BAD):
   score=sum(k in content for k in KEYS)+int('publication' in content or 'cong bo' in content)
   portals.append((score,text,url))
 seen=set(p.get('final_url',p['url']).rstrip('/') for p in result['pages'])
 queue=[]
 for score,text,url in sorted(portals,reverse=True):
  if url.rstrip('/') in seen:continue
  seen.add(url.rstrip('/'));result['research_portal_leads'].append({'title':text[:220],'url':url})
  queue.append(url)
  if len(queue)==2:break
 for url in queue:
  time.sleep(.2)
  page,child_links=fetch(s,url);result['pages'].append(page)
  for text,link in child_links:
   ptext=plain(text)
   if len(text)<45 or len(text)>300 or any(w in ptext for w in BAD):continue
   topics=classify(text)
   if topics==['OTHER']:continue
   if not within(link):continue
   result['research_item_leads'].append({'title':text,'url':link,'found_on':page.get('final_url',url),'topic_codes_auto':topics,'verification':'unreviewed_link_title_not_confirmed_research_item_or_affiliation'})
  # Follow one actual publication/repository link from the research portal.
  if len(result['pages'])<4:
   for text,link in child_links:
    value=plain(text+' '+link)
    if within(link) and any(k in value for k in ['publications','repository','cong-bo-khoa-hoc','cong bo khoa hoc','publikationen']) and link.rstrip('/') not in seen:
     seen.add(link.rstrip('/'));sub,_=fetch(s,link);result['pages'].append(sub);break
 result['research_item_leads']=list({x['url']:x for x in result['research_item_leads']}.values())[:20]
 result['scan_status']='research_links_found' if result['research_portal_leads'] else 'homepage_only_no_research_link_found' if any(p.get('http_status',0)==200 for p in result['pages']) else 'fetch_failed'
 return result

rows=json.loads((ROOT/'scan_candidates.json').read_text());path=ROOT/'portal_scan.jsonl'
done=set()
if path.exists():
 for line in path.read_text().split('\n'):
  try:done.add(json.loads(line)['record_id'])
  except Exception:pass
todo=[r for r in rows if r['record_id'] not in done]
print('Scanning candidates',len(todo),flush=True)
with path.open('a') as f, concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
 tasks={pool.submit(scan,r):r for r in todo}
 for i,future in enumerate(concurrent.futures.as_completed(tasks),1):
  try:result=future.result()
  except Exception as e:result={'record_id':tasks[future]['record_id'],'scan_status':'worker_error','error':str(e)}
  f.write(json.dumps(result,ensure_ascii=False)+'\n');f.flush()
  if i%50==0:print('completed',i,'/',len(todo),flush=True)
print('Complete',flush=True)
