import sys,json,re,csv,hashlib,collections,unicodedata,zipfile
from pathlib import Path
from urllib.parse import unquote
sys.path.insert(0,str(Path(__file__).resolve().parent/'.deps'))
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from ai_config import ROOT,DATE,AI_TOPICS

OUT=ROOT/'ai_deliverables';OUT.mkdir(exist_ok=True)
baseline=json.loads((ROOT/'deliverables/research_classified.json').read_text())
seed={s['short_name']:s for s in baseline['schools']}
order={s['short_name']:i for i,s in enumerate(baseline['schools'])}
def normtitle(t):return re.sub(r'[^\w]+','',unicodedata.normalize('NFKC',t).casefold())
def doi(v):
 if not v:return None
 return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)','',unquote(v).strip(),flags=re.I).lower().rstrip('.')
def identity(w):return 'doi:'+doi(w.get('doi')) if w.get('doi') else 'title:'+normtitle(w['title'])
def tidy(t):
 t=str(t or '')
 t=re.sub(r'(?<=[^\W\d_])(?=20[12]\d\b)',' ',t)
 t=re.sub(r'(?<=[.,;])(?=[A-Za-zÀ-ỹ])',' ',t)
 for a,b in [('thuộcHCMUT','thuộc HCMUT'),('trên tên miềnHCMUT','trên tên miền HCMUT'),('khoVKU','kho VKU'),('báoVKU','báo VKU'),('affiliationHUST','affiliation HUST'),('ECG12','ECG 12'),('mạng5G','mạng 5G')]:t=t.replace(a,b)
 return t

schools=[];associations=[]
for part in ['ai_vn_core','ai_vn_extended','ai_us','ai_eu']:
 doc=json.loads((ROOT/'parts'/f'{part}.json').read_text())
 for rawschool in doc['schools']:
  name=rawschool['short_name'];s=dict(rawschool)
  s.update(country_code=seed[name]['country_code'],region=seed[name]['region'],website=seed[name]['website'])
  s['items']=[]
  for raw in rawschool['items']:
   r=dict(raw)
   r.update(school=name,school_name=s['name'],school_domain=s['domain'],country_code=s['country_code'],region=s['region'])
   r['doi']=doi(r.get('doi'));r['ai_topic_codes']=list(dict.fromkeys(r['ai_topic_codes']))
   r['primary_ai_topic_code']=r.get('primary_ai_topic_code',r['ai_topic_codes'][0])
   r['ai_topic_labels_vi']=[AI_TOPICS[c] for c in r['ai_topic_codes']]
   r['school_attribution']=r.get('school_attribution') or r.get('attribution') or r.get('university_attribution') or r.get('affiliation')
   if not r['school_attribution']:raise ValueError('missing attribution: '+r['title'])
   r['authors']=r.get('authors') or []
   if isinstance(r['authors'],str):r['authors']=[r['authors']]
   r['source_urls']=list(dict.fromkeys([r['url']]+r.get('source_urls',[])))
   r['checked_on']=DATE;r.setdefault('full_text_read',False)
   r['work_key']=identity(r)
   associations.append(r);s['items'].append(r)
  schools.append(s)
schools.sort(key=lambda s:order[s['short_name']])
associations.sort(key=lambda r:(order[r['school']],r['year'] or 0,r['title']))
unique={}
for r in associations:
 k=r['work_key']
 if k not in unique:
  w=dict(r);w['schools']=[];w['institutional_attributions']=[];w['regions']=[];w['country_codes']=[];w['association_ids']=[]
  unique[k]=w
 w=unique[k]
 r['association_id']='A'+str(associations.index(r)+1).zfill(3)
 if r['school'] not in w['schools']:w['schools'].append(r['school'])
 w['institutional_attributions'].append({'school':r['school'],'attribution':r['school_attribution'],'verification_note':r['verification_note'],'source_urls':r['source_urls']})
 w['regions']=list(dict.fromkeys(w['regions']+[r['region']]))
 w['country_codes']=list(dict.fromkeys(w['country_codes']+[r['country_code']]))
 w['ai_topic_codes']=list(dict.fromkeys(w['ai_topic_codes']+r['ai_topic_codes']))
 w['source_urls']=list(dict.fromkeys(w['source_urls']+r['source_urls']))
 w['association_ids'].append(r['association_id'])
works=list(unique.values())
for n,w in enumerate(works,1):
 w['work_id']='AI'+str(n).zfill(3);w['ai_topic_labels_vi']=[AI_TOPICS[c] for c in w['ai_topic_codes']]
 for r in associations:
  if r['work_key']==w['work_key']:r['work_id']=w['work_id']
primary=collections.Counter(w['primary_ai_topic_code'] for w in works)
multi=collections.Counter(c for w in works for c in w['ai_topic_codes'])
coverage=[]
for region in ['Việt Nam','Hoa Kỳ','Châu Âu']:
 ss=[s for s in schools if s['region']==region]
 rr=[r for r in associations if r['region']==region]
 coverage.append({'region':region,'schools':len(ss),'institution_work_records':len(rr),'unique_works_in_region':len(set(r['work_key'] for r in rr))})
base_ai=[w for w in baseline['research_items'] if 'AI_DATA' in w['topic_codes']]
base_keys={identity(w) for w in base_ai};base_titles={normtitle(w['title']) for w in base_ai}
new_count=sum(w['work_key'] not in base_keys and normtitle(w['title']) not in base_titles for w in works)
stats={'date':DATE,'schools':len(schools),'institution_work_records':len(associations),'unique_works':len(works),
 'new_unique_works_vs_previous_detailed_ai_subset':new_count,'ai_topic_groups':len(AI_TOPICS),'regional_coverage':coverage,
 'unique_works_with_doi':sum(bool(w.get('doi')) for w in works),'primary_topic_counts':dict(primary),'multi_label_counts':dict(multi),
 'type_counts':dict(collections.Counter(w['type'] for w in works)),'status_counts':dict(collections.Counter(w['status'] for w in works)),
 'reading_depth_counts':dict(collections.Counter(w['reading_depth'] for w in works)),
 'full_text_read_count':sum(w['full_text_read'] for w in works),
 'schools_without_ai_items':[s['short_name'] for s in schools if not s['items']]}
rules=[
 'Giữ công trình có phương pháp AI cụ thể: học máy/học sâu, mô hình ngôn ngữ, học tăng cường, học biểu diễn, AI tạo sinh, hệ tác tử hoặc suy luận AI. Loại IoT, vật liệu, điều khiển cổ điển và nghiên cứu xã hội về AI nếu nguồn chưa thể hiện đóng góp AI.',
 'Phân loại theo hai trục: nhóm/phương pháp AI và lĩnh vực ứng dụng. Một công trình có thể có nhiều nhãn. Nhãn đa tác tử không tự khẳng định sử dụng LLM; phương pháp chưa rõ được ghi trong phần kiểm chứng.',
 'Đối chiếu quan hệ tác giả–trường bằng affiliation nhà xuất bản, PDF, kho cơ quan hoặc danh mục chính thức. Độ mạnh của bằng chứng được ghi theo từng mục; không coi mọi bài đăng trên tạp chí của trường là của trường.',
 'Gộp bản ghi trùng DOI hoặc tên chuẩn hóa. Công trình hợp tác được liệt kê ở nhiều trường nhưng chỉ tính một lần trong danh mục công trình duy nhất.',
]
limits=[
 'Phạm vi là41 trường của báo cáo trước, ưu tiên Việt Nam, Mỹ và Châu Âu. Đây là tập công trình AI chọn lọc, chưa phải toàn bộ sản lượng của các trường hoặc toàn bộ589 trường trong thống kê ban đầu.',
 'Phần lớn được đọc metadata và abstract; một số có đọc trang đầu hoặc phương pháp chọn lọc, một số chỉ có thư mục/metadata. Không mục nào được khẳng định đã thẩm định toàn văn hay tái lập kết quả.',
 'Giữ riêng bài đã công bố, bài đã chấp nhận, bản tác giả/workshop, luận án, đồ án sinh viên và dự án được phê duyệt/đang triển khai. Không suy ra kết quả đã hoàn thành từ một dự án.',
 'Năm công bố lấy theo nguồn, không suy đoán từ chuỗi DOI. Các khác biệt giữa năm hội nghị, năm số tạp chí và ngày online được giữ trong ghi chú.',
 'Không dùng số công trình trong mẫu để xếp hạng trường hoặc so sánh độ chính xác giữa những bài có dữ liệu/thiết lập khác nhau. Tóm tắt y sinh mô tả nghiên cứu, không xác nhận hiệu quả lâm sàng.',
]
meta={'date':DATE,'statistics':stats,'ai_taxonomy':AI_TOPICS,'selection_rules_vi':rules,'limitations_vi':limits}
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
dump('ai_research_catalog.json',{'metadata':meta,'schools':schools,'unique_works':works,'institution_research_records':associations})
dump('ai_statistics.json',stats)
dump('ai_school_directory.json',{'metadata':meta,'schools':[{k:v for k,v in s.items() if k!='items'}|{'ai_work_ids':list(dict.fromkeys(r['work_id'] for r in s['items']))} for s in schools]})

types={'journal_article':'Bài báo tạp chí','conference_paper':'Bài hội nghị','workshop_paper':'Bài workshop','book_chapter':'Chương sách/kỷ yếu',
 'accepted_conference_paper':'Bài hội nghị đã chấp nhận','doctoral_thesis':'Luận án tiến sĩ','doctoral_dissertation':'Luận án tiến sĩ',
 'student_graduation_project':'Đồ án tốt nghiệp','institutional_research_project':'Đề tài cấp cơ sở','funded_research_project':'Đề tài được tài trợ','technical_report':'Báo cáo kỹ thuật','research_project':'Dự án nghiên cứu'}
depths={'bibliography_only':'Chỉ thư mục/danh mục','source_content_reviewed':'Đã đọc nội dung nguồn theo ghi chú','abstract_and_metadata':'Đã đọc abstract và metadata',
 'abstract_and_metadata_reviewed_previously':'Đã đọc abstract/metadata ở lượt trước','abstract_and_selected_methods':'Abstract và một số phần phương pháp',
 'abstract_and_first_page_affiliations':'Abstract và affiliation trang đầu','abstract_first_page_and_selected_methods':'Abstract, trang đầu và phương pháp chọn lọc',
 'indexed_official_repository_abstract_and_metadata':'Abstract/metadata được lập chỉ mục của kho chính thức'}
status={'published':'Đã công bố','accepted':'Đã chấp nhận; chưa xác nhận xuất bản','thesis_published':'Luận án đã đưa vào kho','published_workshop_paper':'Workshop đã công bố','presented_workshop_paper':'Đã trình bày workshop',
 'approved_project':'Đề tài được phê duyệt','student_project_catalogued':'Đồ án có trong danh mục','public_thesis_pdf_defense_status_not_checked':'Có PDF luận án; chưa kiểm tra trạng thái bảo vệ','ongoing_as_reported_2025_09_22':'Nguồn22/09/2025 ghi đang triển khai'}
def flat(v):
 if v is None:return ''
 if isinstance(v,list):return '; '.join(str(x) for x in v)
 return v
headers=['ID công trình','Trường có liên quan','Tên gốc','Năm','Loại','Trạng thái','Nhóm AI chính','Các nhóm AI','Phương pháp AI','Bài toán nghiên cứu','Lĩnh vực ứng dụng','Tóm tắt','Tác giả','DOI','URL nguồn','Nguồn đối chiếu','Mức đọc','Ghi chú kiểm chứng','Code nếu nguồn nêu','Dữ liệu nếu nguồn nêu']
workrows=[[w['work_id'],w['schools'],w['title'],w['year'],types.get(w['type'],w['type']),status.get(w['status'],w['status']),AI_TOPICS[w['primary_ai_topic_code']],w['ai_topic_labels_vi'],tidy(w['ai_method_vi']),tidy(w['problem_vi']),w['application_domains'],tidy(w['summary_vi']),w['authors'],w.get('doi'),w['url'],w['source_urls'],depths.get(w['reading_depth'],w['reading_depth']),tidy(w['verification_note']),w.get('code_url'),w.get('datasets',[])] for w in works]
with (OUT/'ai_research_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(headers);writer.writerows([[flat(v) for v in r] for r in workrows])
wb=Workbook();wb.remove(wb.active)
def sheet(name,cols,rows,widths=None):
 ws=wb.create_sheet(name);ws.append(cols)
 for row in rows:
  clean=[]
  for v in row:
   v=flat(v)
   if isinstance(v,str):
    v=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',v)[:32700]
    if v.startswith('='):v="'"+v
   clean.append(v)
  ws.append(clean)
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions;ws.sheet_view.showGridLines=False
 for c in ws[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='183B56');c.alignment=Alignment(wrap_text=True)
 ws.row_dimensions[1].height=35
 for n in range(1,len(cols)+1):ws.column_dimensions[get_column_letter(n)].width=(widths or {}).get(n,25)
 for row in ws.iter_rows(min_row=2):
  for c in row:
   c.alignment=Alignment(wrap_text=True,vertical='top')
   if isinstance(c.value,str) and c.value.startswith(('https://','http://')) and '; ' not in c.value and len(c.value)<2000:c.hyperlink=c.value;c.style='Hyperlink'
 return ws
sheet('Huong_dan',['Mục','Nội dung'],[['Phạm vi','Tìm nghiên cứu AI của41 trường đã có trong danh sách.'],['Số liệu',f'{len(works)} công trình duy nhất; {len(associations)} bản ghi trường–công trình; {len(schools)} trường.'],['Cách đọc','Cong_trinh_AI gộp trùng công trình; Theo_truong tra trường và nhóm AI; Ban_ghi_truong giữ bằng chứng riêng từng đơn vị.']]+[[f'Tiêu chí{i+1}',x] for i,x in enumerate(rules)]+[[f'Giới hạn{i+1}',x] for i,x in enumerate(limits)],{1:25,2:125})
sheet('Tong_quan',['Khu vực','Trường','Bản ghi trường–công trình','Công trình duy nhất trong khu vực'],[[r['region'],r['schools'],r['institution_work_records'],r['unique_works_in_region']] for r in coverage],{1:30,3:35,4:40})
sheet('Chu_de_AI',['Mã','Nhóm AI','Nhãn chính: số công trình','Mọi nhãn: số công trình','Trường có ví dụ'],[[c,label,primary[c],multi[c],sorted({r['school'] for r in associations if c in r['ai_topic_codes']})] for c,label in AI_TOPICS.items()],{1:35,2:65,5:110})
sheet('Cong_trinh_AI',headers,workrows,{2:45,3:85,6:40,7:60,8:80,9:100,10:100,11:65,12:105,13:85,14:40,15:90,16:100,17:50,18:120,19:65,20:60})
sheet('Theo_truong',['Trường','Tên đầy đủ','ISO2','Website','Cổng AI/nghiên cứu','Số công trình trong mẫu','Nhóm AI tìm được','Phương pháp trong mẫu','Ghi chú tìm kiếm'],[[s['short_name'],s['name'],s['country_code'],s['website'],[p['url'] if isinstance(p,dict) else p for p in s['ai_portals']],len(s['items']),sorted({AI_TOPICS[c] for r in s['items'] for c in r['ai_topic_codes']}),list(dict.fromkeys(r['ai_method_vi'] for r in s['items'])),tidy(s['search_note_vi'])] for s in schools],{2:60,4:45,5:90,7:90,8:110,9:110})
sheet('Ban_ghi_truong',['ID bản ghi','ID công trình','Trường','ISO2','Tên công trình','Quan hệ tác giả–trường','Nhóm AI','Nguồn','Ghi chú riêng'],[[r['association_id'],r['work_id'],r['school'],r['country_code'],r['title'],tidy(r['school_attribution']),r['ai_topic_labels_vi'],r['source_urls'],tidy(r['verification_note'])] for r in associations],{5:90,6:120,7:80,8:100,9:110})
wb.save(OUT/'bao_cao_nghien_cuu_AI.xlsx')

doc=Document();sec=doc.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65)
sec.header.paragraphs[0].text='NGHIÊN CỨU AI • VIỆT NAM – HOA KỲ – CHÂU ÂU'
doc.styles['Normal'].font.name='Calibri';doc.styles['Normal'].font.size=Pt(10)
for n in ['Title','Heading 1','Heading 2','Heading 3']:doc.styles[n].font.color.rgb=RGBColor.from_string('183B56')
def para(t):return doc.add_paragraph(tidy(t))
def link(p,label,url):
 h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');co=OxmlElement('w:color');co.set(qn('w:val'),'0563C1');pr.append(co);r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)
doc.add_heading('Báo cáo chuyên sâu theo chủ đề AI',0)
para('Ngày tra cứu:30/10/2026. Phạm vi:41 trường trong danh sách đã rà soát.')
para(f'Tập kết quả có {len(works)} công trình AI duy nhất, tương ứng {len(associations)} bản ghi trường–công trình. {new_count} công trình chưa có trong phần AI chi tiết của báo cáo trước. Mỗi trường có ít nhất hai mục được chọn; số mẫu không thể hiện thứ hạng hoặc tổng sản lượng của trường.')
doc.add_heading('1. Phạm vi và phương pháp',1)
for r in rules+limits:para(r)
doc.add_heading('2. Các nhóm chủ đề AI',1)
t=doc.add_table(rows=1,cols=3);t.style='Light Shading Accent 1'
for c,v in zip(t.rows[0].cells,['Nhóm AI','Số công trình có nhãn','Trường có ví dụ']):c.text=v
for code,label in AI_TOPICS.items():
 for c,v in zip(t.add_row().cells,[label,multi[code],', '.join(sorted({r['school'] for r in associations if code in r['ai_topic_codes']}))]):c.text=str(v)
doc.add_heading('3. Kết quả theo từng trường',1)
for n,s in enumerate(schools,1):
 doc.add_heading(f'{n}. {s["name"]}',2)
 p=doc.add_paragraph();p.add_run('Website: ');link(p,s['website'],s['website'])
 for portal in s['ai_portals']:
  p=doc.add_paragraph();link(p,portal.get('title',portal['url']) if isinstance(portal,dict) else portal,portal['url'] if isinstance(portal,dict) else portal)
 para(s['search_note_vi'])
 for r in s['items']:
  doc.add_heading(r['work_id']+' • '+r['title'],3)
  para(f'Năm: {r["year"]} | {types.get(r["type"],r["type"])} | {status.get(r["status"],r["status"])}')
  para('Nhóm AI: '+'; '.join(r['ai_topic_labels_vi']))
  para('Bài toán: '+r['problem_vi']);para('Phương pháp: '+r['ai_method_vi']);para('Nội dung: '+r['summary_vi'])
  if r['authors']:para('Tác giả theo nguồn: '+'; '.join(r['authors']))
  para('Quan hệ với trường: '+r['school_attribution'])
  para('Mức đọc: '+depths.get(r['reading_depth'],r['reading_depth'])+'. '+r['verification_note'])
  p=doc.add_paragraph();link(p,'Nguồn chính',r['url'])
  if r.get('doi'):p.add_run(' | ');link(p,'DOI: '+r['doi'],'https://doi.org/'+r['doi'])
  for u in r['source_urls']:
   if u!=r['url']:
    p=doc.add_paragraph();link(p,'Nguồn đối chiếu: '+u,u)
doc.save(OUT/'bao_cao_nghien_cuu_AI.docx')
with zipfile.ZipFile(ROOT/'bao_cao_AI_cac_truong.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in OUT.iterdir():z.write(f,f.name)
print(json.dumps(stats,ensure_ascii=False,indent=2))
print('Outputs',[(f.name,f.stat().st_size) for f in OUT.iterdir()])
