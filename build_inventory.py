import json, re, hashlib, collections
from urllib.parse import urlsplit
from config import ROOT, DATE, EUROPE, SEEDS, ALIASES, TECH_PATTERN, plain

def host(url):
 try:
  u=urlsplit(url if '://' in url else 'https://'+url)
  return (u.hostname or '').lower().removeprefix('www.')
 except ValueError: return ''

def clean(r):
 r=dict(r);r['website']=r.get('website','').strip()
 if r['website'] and '://' not in r['website']: r['website']='https://'+r['website']
 r['domains']=sorted(set(host(x) for x in r.get('domains',[])+[r['website']] if host(x)))
 r['website_host']=host(r['website'])
 r['source_names']=[r.pop('_source','')]
 r['source_urls']=r.get('source_urls',[])
 r['aliases']=r.get('aliases',[])
 return r

rows=[]
for filename,label in [('vietnam.json','VN-NARIC + school evidence'),('europe_official.json','EQAR-DEQAR + France MESR'),('usa_ipeds.json','NCES IPEDS')]:
 p=ROOT/'parts'/filename
 if p.exists():
  for r in json.loads(p.read_text()):
   r['_source']=label;rows.append(clean(r))

# Preserve separate registry institutions; merge Hipo only when hostname identifies
# exactly one registry row. Shared campuses/ambiguous domains remain distinct.
idx=collections.defaultdict(list)
for i,r in enumerate(rows):
 for d in r['domains']:idx[(r['country_code'],ALIASES.get(d,d))].append(i)
hipo=json.loads((ROOT/'raw/hipo.json').read_text())
for h in hipo:
 r=clean(dict(name=h['name'],country=h['country'],country_code=h['alpha_two_code'],
  website=h['web_pages'][0] if h['web_pages'] else '', alternate_websites=h['web_pages'][1:],
  domains=h['domains'],source_urls=['https://github.com/Hipo/university-domains-list'],
  source_tier='community_directory',institution_type='university_or_college_unverified',
  verification_note='Tên và website từ danh bạ cộng đồng Hipo; chưa xác minh tư cách trường hoặc website hiện hành.',
  _source='Hipo university-domains-list'))
 matches=set(i for d in r['domains'] for i in idx.get((r['country_code'],ALIASES.get(d,d)),[]))
 if len(matches)==1:
  existing=rows[next(iter(matches))]
  existing['aliases']=sorted(set(existing['aliases']+[r['name']]))
  existing['domains']=sorted(set(existing['domains']+r['domains']))
  existing['source_urls']=sorted(set(existing['source_urls']+r['source_urls']))
  existing['source_names']=sorted(set(existing['source_names']+r['source_names']))
 else:
  i=len(rows);rows.append(r)
  for d in r['domains']:idx[(r['country_code'],ALIASES.get(d,d))].append(i)

seedmap={d:(i,n,c) for i,(n,c,d) in enumerate(SEEDS)}
for r in rows:
 seeds=[seedmap[ALIASES.get(d,d)] for d in r['domains'] if ALIASES.get(d,d) in seedmap]
 country=r['country_code']
 r['region']='Việt Nam' if country=='VN' else 'Hoa Kỳ' if country=='US' else 'Châu Âu mở rộng' if country in EUROPE else 'Khu vực khác'
 names=' '.join([r['name'],r.get('english_name',''),r.get('name_official','')]+r.get('aliases',[]))
 r['technology_priority']=bool(seeds or TECH_PATTERN.search(plain(names)))
 r['technology_selection_basis']='user_examples' if seeds else 'name_keyword_candidate' if r['technology_priority'] else 'not_assessed'
 r['is_technology']=None # Name filters are not authoritative institutional classifications.
 r['seed_order']=min(x[0] for x in seeds) if seeds else 99999
 if seeds:r['short_name']=seeds[0][1]
 r['research_scan_status']='pending'
 r['website_verification_status']='registry_listed_not_individually_verified' if r['source_tier']!='community_directory' else 'community_listed_not_verified'
 r['checked_at']=DATE
 r['record_id']=hashlib.sha256((country+'|'+r['name']+'|'+r['website']).encode()).hexdigest()[:16]

priority={'Việt Nam':0,'Hoa Kỳ':1,'Châu Âu mở rộng':2,'Khu vực khác':3}
rows.sort(key=lambda r:(priority[r['region']],r['seed_order'],r['country_code'],plain(r['name'])))
metadata={'retrieved_at':DATE,'record_count':len(rows),'region_counts':dict(collections.Counter(r['region'] for r in rows)),
 'country_count':len(set(r['country_code'] for r in rows)),
 'technology_candidate_count':sum(r['technology_priority'] for r in rows),
 'priority_technology_candidate_count':sum(r['technology_priority'] and r['region']!='Khu vực khác' for r in rows),
 'completeness':'Danh mục tổng hợp, KHÔNG khẳng định đầy đủ 100% hoặc đã xác minh mọi website.',
 'counting_unit':'Bản ghi cơ sở giáo dục, có thể gồm trường thành viên, hệ thống, học viện, college và phân hiệu. Không tương đương số đại học pháp lý độc lập.',
 'technology_filter':'Ví dụ người dùng + từ khóa tên trường đa ngôn ngữ. is_technology=null vì chưa có thẩm định toàn bộ; không suy ra trường không chuyên công nghệ từ việc không khớp tên.',
 'europe_definition':'Phạm vi mở rộng theo dữ liệu EHEA, gồm UK, Thụy Sĩ, Na Uy và các nước xuyên lục địa/Caucasus/Kazakhstan; cột ISO2 cho phép lọc lại.',
 'sources':['https://en.naric.edu.vn/vietnam-recognised-bodies','https://www.eqar.eu/qa-results/download-data-sets/','https://github.com/Hipo/university-domains-list'],
 'source_limitations':'VN-NARIC có lỗi ghép tên-website đã loại các lỗi rõ ràng; NCES không tải được nên Hoa Kỳ chủ yếu dựa Hipo. ROR tải chưa hoàn chỉnh nên không sử dụng làm nguồn bản ghi.'}
(ROOT/'inventory.json').write_text(json.dumps({'metadata':metadata,'universities':rows},ensure_ascii=False,indent=2))
(ROOT/'scan_candidates.json').write_text(json.dumps([r for r in rows if r['technology_priority'] and r['region']!='Khu vực khác'],ensure_ascii=False,indent=2))
print(json.dumps(metadata,ensure_ascii=False,indent=2))
