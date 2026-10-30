import sys,json,re,hashlib,concurrent.futures
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'.deps'))
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from config import ROOT,DATE,classify,TOPICS

out=[]
def add(school,domain,title,year,source,citation='',links=None,authors='',kind='publication_list_entry'):
 title=re.sub(r'\s+',' ',title).strip()
 if len(title)<12:return
 codes=classify(title)
 doi=re.search(r'10\.\d{4,9}/[^\s<>"\]]+', ' '.join(links or []))
 out.append({'school':school,'domain':domain,'country_code':'VN','title':title,'year':year,'type':kind,
 'topic_codes':codes,'topics':[TOPICS[x][0] for x in codes],
 'classification_method':'Tự động theo từ khóa trong tiêu đề; cần rà soát chuyên môn. Không tương đương phân loại thủ công.',
 'source_url':source,'publication_urls':links or [],'doi':doi.group(0).rstrip('.,;') if doi else None,
 'authors_as_listed':authors,'citation_as_listed':citation,
 'verification_note':'Đã trích bản ghi thư mục từ danh sách/kho của trường; chưa đọc abstract/toàn văn, chưa đối chiếu toàn bộ affiliation hoặc tình trạng xuất bản.',
 'checked_on':DATE,'full_text_read':False})

u='https://soict.hust.edu.vn/en/2025-publications.html'
s=BeautifulSoup((ROOT/'raw/hust_soict.html').read_bytes(),'html.parser')
unparsed=[]
for li in s.select('ol li'):
 text=li.get_text(' ',strip=True)
 match=re.search('[“"]([^”"]+)[”"]',text)
 if not match:unparsed.append(text);continue
 title=match.group(1);year_match=re.search(r'\b(20\d\d)\b',text[match.end():]);year=int(year_match.group(1)) if year_match else 2025
 add('HUST','hust.edu.vn',title,year,u,text,[a['href'] for a in li.select('a[href]')],text[:match.start()].strip(' .'))

u='https://tel.ptit.edu.vn/nghien-cuu/bai-bao-tap-chi-trong-nuoc/'
s=BeautifulSoup((ROOT/'raw/ptit_tel.html').read_bytes(),'html.parser')
for tr in s.select('table tr'):
 cells=[x.get_text(' ',strip=True) for x in tr.select('td')]
 if len(cells)<7 or not re.fullmatch(r'20\d\d',cells[1]):continue
 add('PTIT','ptit.edu.vn',cells[2],int(cells[1]),u,' | '.join(cells),[a['href'] for a in tr.select('a[href]')],cells[3],'journal_article_listed')

# Public repository collection listings: titles/author/year only, no full-text copying.
base='https://elib.vku.udn.vn/handle/123456789/5064'
def fetch_page(offset):
 u=base+'?offset='+str(offset)
 try:
  r=requests.get(u,timeout=15);r.raise_for_status();s=BeautifulSoup(r.content,'html.parser')
  records=[]
  for tr in s.select('table tr'):
   cells=tr.select('td')
   if len(cells)<3:continue
   date=cells[0].get_text(' ',strip=True);a=cells[1].find('a',href=True)
   if not a or not re.match('2025',date):continue
   records.append((a.get_text(' ',strip=True),urljoin(u,a['href']),cells[2].get_text(' ',strip=True)))
  return records
 except Exception as e:return []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for records in ex.map(fetch_page,[0,20,40,60,80,100]):
  for title,url,authors in records:add('VKU','vku.udn.vn',title,2025,url,authors=authors,kind='repository_publication_record')

dedup={}
for r in out:
 key=r['domain']+'|'+re.sub(r'\W+','',r['title'].lower())
 if key not in dedup:dedup[key]=r
out=list(dedup.values())
(ROOT/'bibliography_classified.json').write_text(json.dumps({'checked_on':DATE,'classification_level':'automatic_title_keywords_needs_review','records':out,'unparsed_hust_citations_count':len(unparsed)},ensure_ascii=False,indent=2))
print('records',len(out),'schools',{x:sum(r['school']==x for r in out) for x in ['HUST','PTIT','VKU']},'unparsed',len(unparsed))
