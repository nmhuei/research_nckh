import json,re,collections,pathlib
from urllib.parse import urlparse
p=pathlib.Path('/home/ubuntu/university_research/parts');raw=json.loads((p/'vietnam_naric_raw.json').read_text()); groups={};rejected=[]
alias={'en.tnus.edu.vn':'tnus.edu.vn','oude.edu.vn':'ou.edu.vn','hufi.edu.vn':'huit.edu.vn','husc.hueuni.edu.vn':'husc.edu.vn','hucfl.hueuni.edu.vn':'huflis.edu.vn','vanlanguni.edu.vn':'vlu.edu.vn','dhsptn.edu.vn':'tnue.edu.vn','nuce.edu.vn':'huce.edu.vn','www1.napa.vn':'napa.vn','portal.ptit.edu.vn':'ptit.edu.vn','hocvientoaan.edu.vn':'hvta.toaan.gov.vn','fpt.edu.vn':'daihoc.fpt.edu.vn','www,lqdtu.edu.vn':'mta.edu.vn'}
for r in raw:
 d=r['domains'][0].strip().removeprefix('www.');n=r['name'].casefold()
 reason=None
 if d=='hcmiu.edu.vn' and not ('quốc tế' in n and ('hồ chí minh' in n or n.strip()=='trường đại học quốc tế')):reason='Registry incorrectly repeats International University website across unrelated historic institutions.'
 if d=='hpmu.edu.vn' and 'nông lâm' in n:reason='Registry mismatch: Thai Nguyen agriculture institution incorrectly linked to Hai Phong medical university.'
 if d in ['ydmekong.edu.vn','molisa.gov.vn','httt']:reason='Invalid or clearly unrelated registry website; excluded.'
 if reason:rejected.append({'record':r,'reason':reason});continue
 original=d
 if ';' in d:d=d.split(';')[0]
 if d=='dhktna.edu.vn':d='naue.edu.vn'
 d=alias.get(d,d)
 if not re.match(r'^[a-z0-9.-]+\.[a-z]{2,}$',d):rejected.append({'record':r,'reason':'Malformed host.'});continue
 r['website']='https://'+d+'/' if original!=d or ' ' in r['website'] or ';' in r['website'] else r['website']
 r['domains']=[d]
 if original!=d and re.match(r'^[a-z0-9.-]+\.[a-z]{2,}$',original):r['domains'].append(original)
 if d not in groups:groups[d]=r;r['aliases']=[]
 else:
  x=groups[d];x['aliases']=list(dict.fromkeys(x['aliases']+[r['name']]));x['source_urls']=list(dict.fromkeys(x['source_urls']+r['source_urls']));x['domains']=list(dict.fromkeys(x['domains']+r['domains']))
  if d=='hpmu.edu.vn' and 'y dược' in n:x['name']=r['name']
for d in ['hcmiu.edu.vn','hpmu.edu.vn']:
 groups[d]['verification_note']+=' Excluded demonstrably mismatched source rows for this domain.'
fixes={
'huce.edu.vn':('Trường Đại học Xây dựng Hà Nội','university'),
'mta.edu.vn':('Học viện Kỹ thuật Quân sự (Đại học Kỹ thuật Lê Quý Đôn)','academy'),
'vlute.edu.vn':('Trường Đại học Công nghệ Kỹ thuật Vĩnh Long','university'),
'vnam.edu.vn':('Học viện Âm nhạc Quốc gia Việt Nam','academy'),
'hocvienpkkq.com':('Học viện Phòng không - Không quân','academy'),
'phuxuan.edu.vn':('Trường Đại học Phú Xuân','university'),
'is.vnu.edu.vn':('Trường Quốc tế - Đại học Quốc gia Hà Nội','constituent_school'),
'ptit.edu.vn':('Học viện Công nghệ Bưu chính Viễn thông','academy'),
'daihoc.fpt.edu.vn':('Trường Đại học FPT','university')}
for d,(name,typ) in fixes.items():
 if d in groups:
  r=groups[d];r['aliases']=list(dict.fromkeys(r['aliases']+[r['name']]));r['name']=name;r['institution_type']=typ
  r['source_urls'].append('https://'+d+'/');r['verification_note']+=' Canonical institutional domain/name normalization; historic variants retained as aliases.'
# KMA link is missing/incorrect in registry. Use institution's official site.
groups['actvn.edu.vn']={'name':'Học viện Kỹ thuật Mật mã','english_name':'Academy of Cryptography Techniques','short_name':'KMA','country':'Viet Nam','country_code':'VN','website':'https://actvn.edu.vn/','domains':['actvn.edu.vn'],'source_urls':['https://actvn.edu.vn/','https://actvn.edu.vn/Images/Uploadfiles/To%C3%A0n%20v%C4%83n%20Lu%E1%BA%ADn%20%C3%81n.pdf'],'source_tier':'institution_official','verification_note':'Official institution website and doctoral thesis hosted on same domain; replaces erroneous registry mapping to hcmiu.edu.vn.','institution_type':'academy'}
for d in ['vnu.edu.vn','vnuhcm.edu.vn','tnu.edu.vn','udn.vn','hueuni.edu.vn']:groups[d]['institution_type']='university_system'
for d in ['smp.udn.vn','vnuk.udn.vn']:groups[d]['institution_type']='constituent_school_or_institute'
for d in ['hcma1.hcma.vn']:groups[d]['institution_type']='regional_academy'
# Interior university merged into NAPA; retain as historical rather than count as current separate university.
if 'truongnoivu.edu.vn' in groups:groups['truongnoivu.edu.vn']['institution_type']='historical_institution';groups['truongnoivu.edu.vn']['verification_note']+=' Historical institution; current independent status not asserted.'
records=sorted(groups.values(),key=lambda r:r['name'].casefold())
(p/'vietnam.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(p/'vn_sources'/'naric_rejected_mapping_rows.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=2))
notes={'retrieved_at':'2026-10-30','record_count':len(records),'primary_source':'https://en.naric.edu.vn/vietnam-recognised-bodies','secondary_reference':'https://vqa.moet.gov.vn/vi/thong-bao-quan-ly-bao-dam/','extraction':'Downloaded public VN-NARIC HTML pages 0..37 and extracted table name, English name, short name, website and address. Excluded college and vocational rows; merged identical hosts and known historical/alternate domains; added KMA official domain; retained provenance per record.','source_rows_downloaded':750,'raw_name_domain_pairs_before_cleaning':len(raw),'rejected_incorrect_mapping_pairs':len(rejected),'limitations':['Not a claim of a complete current legal institution census. Registry mixes historical names, duplicate records, branches, constituent schools and tertiary/vocational providers.','Registry contains substantive errors: hcmiu.edu.vn reused for dozens of unrelated institutions; hpmu.edu.vn reused for Thai Nguyen agriculture; these erroneous mappings removed, not trusted merely because source official.','Page0 and page1 return same rows; last pages overlap; published row numbers start21. First20 records cannot be confirmed from pagination.','TLS certificate for en.naric.edu.vn has hostname mismatch; read-only public fetch used verify=False, content provenance preserved.','Institution websites not individually inspected for all rows; HTTP retrieval status does not establish current accreditation, degree authority, completeness or name currency.','Historical/alternate domains retained as aliases where known; some renamed/merged institutions remain requiring review.','University systems and member institutions are separate records; branch and constituent types marked when apparent.'],'institution_type_counts':dict(collections.Counter(r['institution_type'] for r in records)),'files':{'raw_pages':'parts/vn_sources/naric*.html','raw_rows':'parts/vn_sources/naric_all_rows.json','rejected_mappings':'parts/vn_sources/naric_rejected_mapping_rows.json','extract_script':'parts/extract_vietnam.py','clean_script':'parts/clean_vietnam.py'}}
(p/'vietnam_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print(json.dumps(notes,ensure_ascii=False,indent=2))
