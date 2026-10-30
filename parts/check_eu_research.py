import json,sys,collections,re,concurrent.futures,requests,unicodedata
from pathlib import Path
sys.path.insert(0,'/home/ubuntu/university_research')
from config import TOPICS
p=Path('/home/ubuntu/university_research/parts/eu_research.json');d=json.loads(p.read_text())
mp={'AI & dữ liệu':'AI_DATA','An toàn thông tin':'CYBERSECURITY','Điện tử & viễn thông':'ELECTRONICS_TELECOM','Robot & tự động hóa':'ROBOTICS','Vật liệu':'MATERIALS','Năng lượng':'ENERGY','Môi trường':'ENVIRONMENT','Công nghệ sinh học & y sinh':'BIOTECH_HEALTH','Xây dựng & giao thông':'CONSTRUCTION_TRANSPORT','Khoa học cơ bản':'BASIC_SCIENCE'}
primary=['ROBOTICS','ROBOTICS','ENERGY','MATERIALS','ENERGY','AI_DATA','ROBOTICS','ROBOTICS','ELECTRONICS_TELECOM','ELECTRONICS_TELECOM','ENERGY','ROBOTICS','AI_DATA','MATERIALS','ROBOTICS','ROBOTICS','CYBERSECURITY','CYBERSECURITY','ENERGY','ENERGY','ELECTRONICS_TELECOM','ELECTRONICS_TELECOM','ENERGY','ENERGY','ROBOTICS','ROBOTICS','BASIC_SCIENCE','ENERGY']
items=[i for s in d['schools'] for i in s['items']]
assert len(primary)==len(items)==28
for i,code in zip(items,primary):
 i['topic_codes']=[mp[t] for t in i['topics']]
 i['primary_topic_code']=code
 assert code in TOPICS and code in i['topic_codes']
 i['retrieved_on']='2026-10-30'
 i['source_kind']='official_project_announcement' if i['type']=='research_project' else ('publisher_and_university' if i.get('attribution_url') and i['url'].startswith('https://www.nature.com/') else 'official_university_repository')
for s in d['schools']:
 assert len(s['items'])>=2
 assert len({i['title'] for i in s['items']})==len(s['items'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))

def chk(i):
 if not i['doi']:return {'title':i['title'],'status':'no_doi_in_read_metadata'}
 try:
  r=requests.get('https://api.crossref.org/works/'+i['doi'],timeout=20,headers={'User-Agent':'UniversityResearchMetadataCheck/1.0'})
  if r.status_code!=200:return {'title':i['title'],'doi':i['doi'],'status':r.status_code}
  m=r.json()['message']; years={k:m[k].get('date-parts') for k in ['published','published-online','published-print','issued'] if k in m}
  actual=m.get('title',[''])[0]
  def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).lower())
  return {'title':i['title'],'doi':i['doi'],'status':'ok','crossref_title':actual,'exact_title_normalized_match':norm(actual)==norm(i['title']),'dates':years,'record_year':i['year']}
 except Exception as e:return {'title':i['title'],'doi':i['doi'],'status':'request_error','detail':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:checks=list(ex.map(chk,items))
Path('/home/ubuntu/university_research/parts/eu_research_checks.json').write_text(json.dumps({'checked_on':'2026-10-30','checks':checks},ensure_ascii=False,indent=2))
print(json.dumps({'schools':len(d['schools']),'items':len(items),'codes_valid':True,'statuses':dict(collections.Counter(str(x['status']) for x in checks)),'title_mismatches':[x for x in checks if x.get('exact_title_normalized_match')==False]},ensure_ascii=False,indent=2))
