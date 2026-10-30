import json,copy
from ai_config import ROOT,DATE

d=json.loads((ROOT/'deliverables/research_classified.json').read_text())
old={w['record_id']:w for w in d['research_items']}
schools=[]
for s in d['schools'][:9]:
 schools.append({'short_name':s['short_name'],'name':s['name'],'domain':s['domain'],'ai_portals':s['research_portals'],'items':[],
 'search_note_vi':'Tìm công trình AI trên nguồn trường, nhóm nghiên cứu và nhà xuất bản; các hướng chỉ phản ánh các công trình được chọn.'})
by={s['short_name']:s for s in schools}
def existing(code,rid,method,problem,cats,domains):
 w=copy.deepcopy(old[rid]);w.update(ai_method_vi=method,problem_vi=problem,ai_topic_codes=cats,application_domains=domains,
  school_attribution=w.get('university_attribution','Nguồn khoa/phòng thí nghiệm hoặc thông tin tác giả được ghi trong ghi chú kiểm chứng.'),
  reading_depth=w.get('evidence_level','source_content_reviewed'),status='accepted' if w['type']=='accepted_conference_paper' else 'published',checked_on=DATE)
 w['source_record_id']=w.pop('record_id');by[code]['items'].append(w);return w
def new(code,title,year,kind,cats,domains,method,problem,summary,url,doi=None,authors=None,note='',sources=None,depth='abstract_and_metadata',status='published',**extra):
 w={'title':title,'year':year,'type':kind,'status':status,'authors':authors or [],'ai_topic_codes':cats,'application_domains':domains,
  'ai_method_vi':method,'problem_vi':problem,'summary_vi':summary,'url':url,'doi':doi,'source_urls':list(dict.fromkeys([url]+(sources or []))),
  'verification_note':note,'reading_depth':depth,'checked_on':DATE,'full_text_read':False,**extra}
 by[code]['items'].append(w);return w

# USTH: explicit publisher metadata establishes both authorship and affiliation.
meta_url='https://api.crossref.org/works/10.1145/3654796'
new('USTH','A Novel Pretrained General-purpose Vision Language Model for the Vietnamese Language',2024,'journal_article',
 ['VISION_MULTIMODAL','NLP_SPEECH','ML_FOUNDATIONS'],['Tiếng Việt','Hỏi đáp bằng ảnh','Sinh chú thích ảnh'],
 'VisualRoBERTa kết hợp CNN và Transformer, tiền huấn luyện ảnh–văn bản rồi tinh chỉnh cho VQA và sinh chú thích.',
 'Xây dựng mô hình ảnh–ngôn ngữ cho tiếng Việt khi dữ liệu và mô hình nền tảng còn hạn chế.',
 'Giới thiệu VisualRoBERTa và dữ liệu ảnh–chú thích dịch sang tiếng Việt; đánh giá hỏi đáp ảnh và sinh chú thích ảnh.',
 'https://dl.acm.org/doi/10.1145/3654796','10.1145/3654796',['Dinh Anh Vu','Quang Nhat Minh Pham','Giang Son Tran'],
 'Đọc abstract và metadata do ACM gửi Crossref; ACM trực tiếp trả403. Crossref ghi Dinh Anh Vu và Giang Son Tran thuộc USTH, Quang Nhat Minh Pham thuộc Aimesoft. Không đọc toàn văn.',
 sources=[meta_url,'https://www.sontg.net/'],school_attribution='Hai tác giả có affiliation USTH trong metadata nhà xuất bản/Crossref.')
new('USTH','Apply a CNN-Based Ensemble Model to Chest-X Ray Image-Based Pneumonia Classification',2024,'journal_article',
 ['HEALTH_BIOAI','VISION_MULTIMODAL'],['Ảnh X-quang','Hỗ trợ phân loại viêm phổi'],
 'Học tổ hợp các CNN InceptionResNetV2, DenseNet201 và VGG16.',
 'Phân biệt ảnh X-quang có dấu hiệu viêm phổi và ảnh bình thường.',
 'So sánh mô hình CNN đơn lẻ với mô hình tổ hợp để phân loại ảnh ngực; đây là đánh giá nghiên cứu, chưa xác nhận triển khai lâm sàng.',
 'https://www.jait.us/show-246-1597-1.html','10.12720/jait.15.11.1205-1214',['Ngoc Ha Pham','Giang Son Tran'],
 'Đã đọc abstract và affiliation trên trang nhà xuất bản. Ngoc Ha Pham đồng thời thuộc USTH và FPT; Giang Son Tran thuộc USTH. Không đọc toàn văn.',
 school_attribution='Affiliation công khai xác nhận USTH và đồng tác giả FPT.',published_date='2024-11-08')
new('USTH','Pneu-ConViT: A CLAHE-Enhanced Hybrid CNN–Vision Transformer Ensemble for Pneumonia Classification',2026,'journal_article',
 ['HEALTH_BIOAI','VISION_MULTIMODAL'],['Ảnh y khoa','X-quang ngực'],
 'Tiền xử lý CLAHE và kết hợp nhiều CNN với Vision Transformer; giải thích bằng Grad-CAM và attention.',
 'Cải thiện phân loại ảnh viêm phổi và kiểm tra khả năng chuyển sang bộ dữ liệu khác.',
 'Kết hợp đặc trưng cục bộ của CNN và ngữ cảnh toàn cục của ViT; đánh giá trên Kermany và kiểm tra ngoài bộ dữ liệu bằng RSNA.',
 'https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/ipr2.70434','10.1049/ipr2.70434',['Ngoc Ha Pham','Giang Son Tran','Antoine Doucet'],
 'Đọc abstract và một số phần phương pháp qua chỉ mục nhà xuất bản; đối chiếu affiliation và ngày online17/07/2026 từ Crossref. Các phiên bản metadata/nội dung có khác biệt số đo, nên không chép chỉ số hiệu năng vào bản tóm tắt. Chưa thẩm định toàn văn.',
 sources=['https://api.crossref.org/works/10.1049/ipr2.70434'],depth='abstract_and_selected_methods',
 school_attribution='Metadata nhà xuất bản xác nhận USTH, FPT và La Rochelle.',published_date='2026-07-17')

# HUST: two existing specific AI papers plus one newly read primary publication.
existing('HUST','T005','Mạng thích nghi miền học sâu kết hợp hàm đặc trưng trơn.','Phân loại lưu lượng mã hóa trong các miền dữ liệu khác nhau.',
 ['SECURITY_TRUST_PRIVACY','ML_FOUNDATIONS'],['An ninh mạng','Phân tích lưu lượng'])
existing('HUST','T006','Học tổ hợp sâu và mô hình ngôn ngữ lập trình.','Phát hiện code smell tự động để hỗ trợ đánh giá chất lượng mã nguồn.',
 ['LLM_RAG_AGENTS','SCIENTIFIC_INDUSTRIAL_AI'],['Kỹ thuật phần mềm'])
new('HUST','Certified Unlearning for Federated Recommendation',2025,'journal_article',
 ['SECURITY_TRUST_PRIVACY','FORECAST_RECOMMEND','ML_FOUNDATIONS'],['Hệ gợi ý','Học liên kết','Quyền riêng tư'],
 'CFRU loại ảnh hưởng cập nhật của người dùng, lấy mẫu lịch sử cập nhật quan trọng và bù sai lệch bằng ước lượng có bảo đảm.',
 'Xóa đóng góp của người dùng khỏi hệ gợi ý liên kết mà không phải huấn luyện lại từ đầu.',
 'Đề xuất cơ chế unlearning cho hệ gợi ý liên kết, phân tích sai lệch và đánh giá trên MovieLens/Pinterest với mô hình NCF và LightGCN.',
 'https://dl.acm.org/doi/10.1145/3706419','10.1145/3706419',
 ['Thanh Trung Huynh','Trong Bang Nguyen','Thanh Toan Nguyen','Phi Le Nguyen','Hongzhi Yin','Quoc Viet Hung Nguyen','Thanh Tam Nguyen'],
 'Đọc abstract và các phần mô tả cơ chế/thực nghiệm trên trang ACM công khai. HUST xác nhận trong danh mục SoICT2025; đây là công trình hợp tác. Không tái lập kết quả.',
 sources=['https://soict.hust.edu.vn/en/2025-publications.html'],depth='abstract_and_selected_methods',
 school_attribution='Danh mục công bố chính thức SoICT HUST liệt kê công trình và nhóm tác giả.',code_url='https://github.com/thanhtrunghuynh93/CFRU',datasets=['MovieLens','Pinterest'],published_date='2025-01-17')

# UET: retain publisher-verified affiliations rather than assigning all a lecturer's publications to UET.
existing('UET','T007','Tinh chỉnh mô hình ngôn ngữ và Retrieval-Augmented Generation.','So sánh hai cách thích ứng LLM với văn bản luật tiếng Việt.',
 ['LLM_RAG_AGENTS','NLP_SPEECH'],['Tiếng Việt','Tra cứu pháp luật'])
existing('UET','T008','Lập kế hoạch đa tác tử và truy xuất tri thức động từ cơ sở dữ liệu, nhật ký hỏi đáp và web.',
 'Trả lời câu hỏi sản phẩm phức tạp bằng cách chia nhỏ tác vụ và tìm bằng chứng phù hợp.',
 ['LLM_RAG_AGENTS','NLP_SPEECH'],['Hỏi đáp sản phẩm','Thương mại điện tử'])
by['UET']['search_note_vi']+=' Không gán ViLLM-Eval cho UET vì chưa thấy affiliation UET trong bản bài báo, dù có tên trong danh mục cá nhân giảng viên.'

existing('HCMUT','T009','Học tăng cường sâu cho bài toán lập lịch tác vụ.','Cải thiện hiệu quả chi phí và sử dụng tài nguyên hệ thống tính toán hiệu năng cao.',
 ['ROBOTICS_RL','EDGE_SYSTEMS'],['Siêu máy tính','Lập lịch'])
existing('HCMUT','T010','Sentence-BERT tinh chỉnh và nhúng đặc trưng văn bản.','Dự đoán kết quả tác vụ HPC từ dữ liệu mô tả tác vụ.',
 ['NLP_SPEECH','EDGE_SYSTEMS'],['Siêu máy tính','Dự đoán tác vụ'])
by['HCMUT']['search_note_vi']+=' Hai mục HPCC mới ở mức danh mục phòng thí nghiệm; chưa đọc abstract/toàn văn. Không đưa bài cảng container vào vì affiliation tại thời điểm công bố chưa được xác nhận.'

existing('UIT','T012','Hợp nhất bộ mã hóa CLIP, OCR, nhận dạng tiếng nói và mô hình thị giác–ngôn ngữ.','Tìm kiếm và hỏi đáp video đa phương thức theo truy vấn người dùng.',
 ['VISION_MULTIMODAL','NLP_SPEECH','LLM_RAG_AGENTS'],['Tìm kiếm video','Truy xuất thông tin'])
existing('UIT','T013','Mô hình ngôn ngữ cho mã nguồn, kiểm tra độ bền vững và Explainable AI.',
 'Kiểm tra liệu phát hiện lỗ hổng và giải thích của mô hình còn ổn định khi mã nguồn bị viết lại.',
 ['SECURITY_TRUST_PRIVACY','LLM_RAG_AGENTS'],['An ninh phần mềm'])

existing('PTIT','T015','Khung AI đa tác tử phối hợp phân tích dữ liệu và cảnh báo.','Tự động phát hiện lỗ hổng và tạo cảnh báo an ninh mạng.',
 ['LLM_RAG_AGENTS','SECURITY_TRUST_PRIVACY'],['An ninh mạng'])
by['PTIT']['items'][-1]['verification_note']+=' Nguồn gọi là multi-agent AI nhưng chưa công khai rõ mô hình nền hay LLM; nhãn hệ đa tác tử không khẳng định sử dụng một LLM cụ thể.'
new('PTIT','MULTI-LEVEL STACKING ENSEMBLE LEARNING FOR ENHANCED ECG-BASED ARRHYTHMIA DETECTION',2025,'journal_article',
 ['HEALTH_BIOAI','FORECAST_RECOMMEND'],['Điện tâm đồ','Phân loại rối loạn nhịp'],
 'Stacking nhiều tầng với Random Forest, XGBoost, SVM, KNN, AdaBoost, Decision Tree và mô hình tổng hợp Logistic Regression.',
 'Phân loại rối loạn nhịp từ dữ liệu ECG12 chuyển đạo.',
 'Kết hợp dự đoán của nhiều bộ phân loại để khai thác tín hiệu ECG; abstract báo cáo so sánh các thước đo phân loại.',
 'https://tapchi.ptit.edu.vn/jstic-ptit/index.php/jstic/article/view/1676',authors=['Huu-Cam Nguyen','Thu-Trang T. Nguyen','Hai-Long Nguyen','Ngoc-Anh T. Phung','Anh-Thu Pham'],
 note='Đã đọc abstract trang tạp chí và trang đầu PDF xác nhận các tác giả thuộc PTIT. Trang ghi published15/09/2025 nhưng số tạp chí/PDF ghi2024; năm chính lấy ngày online, giữ năm số tạp chí ở alternative_years. Chưa đọc toàn văn.',
 sources=['https://jstic.ptit.edu.vn/jstic-ptit/index.php/jstic/article/download/1676/486/6594'],school_attribution='Trang đầu PDF ghi Posts and Telecommunications Institute of Technology, Hanoi, Vietnam.',alternative_years=[2024],published_date='2025-09-15')
existing('PTIT','T016','Mô hình học máy dự báo trạng thái môi trường; danh mục chưa nêu kiến trúc cụ thể.',
 'Dự báo môi trường nhà kính để hỗ trợ giám sát nông nghiệp.',
 ['FORECAST_RECOMMEND','SCIENTIFIC_INDUSTRIAL_AI'],['Nông nghiệp thông minh','Nhà kính'])

existing('DUT','T017','Xử lý ảnh và bộ nhận dạng AI cho tư thế sản phẩm; abstract chưa nêu kiến trúc mô hình.',
 'Robot xác định loại bao gói và tư thế lon trên băng chuyền để gắp đúng vị trí.',
 ['VISION_MULTIMODAL','ROBOTICS_RL'],['Tự động hóa sản xuất'])
new('DUT','Hybrid deep learning model for improving the operational efficiency of microgrids',2025,'journal_article',
 ['FORECAST_RECOMMEND','SCIENTIFIC_INDUSTRIAL_AI','ML_FOUNDATIONS'],['Điện gió','Điện mặt trời','Lưới điện nhỏ'],
 'Kết hợp LSTM với Inductive Conformal Prediction để dự báo kèm khoảng tin cậy.',
 'Dự báo công suất tái tạo theo nhiều chân trời và biểu diễn độ bất định phục vụ vận hành microgrid.',
 'Đánh giá LSTM+ICP trên dữ liệu nhà máy điện gió và mặt trời ở Việt Nam, đối chiếu Random Forest và LSTM cơ sở.',
 'https://jst-ud.vn/jst-ud/article/view/9828','10.31130/ud-jst.2025.23(6A).214E',
 ['Hong Duy An Nguyen','Trong Nhan Van','Thi Cat Tuong Nguyen','Ngoc Thien Nam Tran','Minh Quan Duong'],
 'Đã đọc abstract, affiliation và ngày xuất bản30/06/2025. Bốn tác giả thuộc DUT, một tác giả Delta Electronic. Chưa đọc toàn văn.',
 school_attribution='Affiliation tác giả trên trang tạp chí xác nhận DUT.',published_date='2025-06-30')

existing('VKU','T019','CNN/RNN/LSTM/BiLSTM/MLP kết hợp Walrus Optimization cho lựa chọn siêu tham số.',
 'Ước lượng nỗ lực phát triển phần mềm bằng mô hình học sâu tối ưu.',
 ['SCIENTIFIC_INDUSTRIAL_AI','FORECAST_RECOMMEND'],['Kỹ thuật phần mềm','Ước lượng chi phí'])
existing('VKU','T020','CNN xử lý ảnh kết hợp Random Forest trên dữ liệu cảm biến môi trường.',
 'Kết hợp hai nguồn dữ liệu để phát hiện cháy và giảm báo động giả.',
 ['VISION_MULTIMODAL','EDGE_SYSTEMS'],['Phòng cháy','IoT'])
new('VKU','A Novel Hybrid Deep Learning Framework for Automated Malaria Parasite Detection in Microscopic Blood Smear Images',2025,'conference_paper',
 ['HEALTH_BIOAI','VISION_MULTIMODAL'],['Ảnh kính hiển vi','Sốt rét'],
 'CNN trích đặc trưng, chọn đặc trưng bằng Levy-flight Grey Wolf Optimization rồi phân loại SVM.',
 'Phát hiện ký sinh trùng sốt rét từ ảnh tiêu bản máu.',
 'Đề xuất chuỗi tiền xử lý, trích/chọn đặc trưng và phân loại; abstract báo cáo đánh giá trên các bộ dữ liệu ảnh sốt rét công khai.',
 'https://elib.vku.udn.vn/handle/123456789/7671','10.1007/978-3-032-10209-6_17',['Vu Thu Nguyet Pham','Quang Vu Nguyen'],
 'Đọc metadata/abstract từ khoVKU, ICCCI2025. Toàn văn yêu cầu đăng nhập; quy thuộc qua bộ sưu tập cơ quan, chưa đối chiếu trang affiliation của PDF.',
 school_attribution='Kho tài nguyên sốVKU, bộ sưu tập bài báo2025.')
new('VKU','DWACE: Enhancing Graph Clustering via Autoencoder and Contrastive Learning Refinement of DeepWalk Embeddings',2025,'conference_paper',
 ['ML_FOUNDATIONS'],['Phân cụm đồ thị','Học biểu diễn'],
 'Autoencoder phi tuyến khử nhiễu/nén nhúng DeepWalk, kết hợp mục tiêu contrastive learning.',
 'Giảm nhiễu và dư thừa của biểu diễn nút nhằm cải thiện phân cụm cộng đồng đồ thị.',
 'Kết hợp bảo toàn cấu trúc đồ thị và tính nhất quán của biểu diễn; abstract nêu đánh giá trên năm bộ dữ liệu chuẩn.',
 'https://elib.vku.udn.vn/handle/123456789/7667','10.1007/978-981-95-3358-9_27',
 ['Nguyen Xuan Thao Mai','Cong Phap Huynh','Kunchan Supeeti','Dai Tho Dang'],
 'Đọc metadata/abstract khoVKU. Năm2025 theo hội nghị/bộ sưu tập; chưa đối chiếu năm phát hành sách Springer. Trường trang trong kho có lỗi372–338 nên không sử dụng.',
 school_attribution='Kho tài nguyên sốVKU, bộ sưu tập bài báo2025.')

existing('HCMUTE','T021','DomBert biểu diễn theo miền, GCN trích đặc trưng, hợp nhất bộ phân loại.',
 'Phân tích cảm xúc có xét khác biệt miền dữ liệu.',
 ['NLP_SPEECH','ML_FOUNDATIONS'],['Phân tích cảm xúc'])
new('HCMUTE','Enhanced Monthly Load Forecasting With RapidMiner-Based Deep Learning',2026,'journal_article',
 ['FORECAST_RECOMMEND','SCIENTIFIC_INDUSTRIAL_AI'],['Dự báo phụ tải điện','Hệ thống điện'],
 'Mạng học sâu trên RapidMiner với dữ liệu tiêu thụ điện và thời tiết.',
 'Dự báo phụ tải điện ngày qua nhiều tháng để hỗ trợ lập kế hoạch vận hành.',
 'Huấn luyện và kiểm tra mô hình trên một nghiên cứu trường hợp tại TP.HCM; so sánh với Decision Tree và SVM.',
 'https://www.jte.edu.vn/index.php/jte/article/view/1901','10.54644/jte.2025.1901',['Gia-Tue Tang','Dinh-Nhon Truong'],
 'Đọc abstract, affiliation và metadata. Trang ghi xuất bản28/08/2026, số21(03)2026; DOI chứa2025 không được dùng để suy ra năm công bố. Chưa đọc toàn văn.',
 school_attribution='Trang tác giả xác nhận cả hai thuộc HCM-UTE.',published_date='2026-08-28')
by['HCMUTE']['ai_portals'].append({'title':'Computer Vision & Intelligent Systems Laboratory','url':'https://cvis.hcmute.edu.vn/Research'})

assert len(schools)==9 and all(len(s['items'])>=2 for s in schools)
(ROOT/'parts/ai_vn_core.json').write_text(json.dumps({'checked_on':DATE,'schools':schools},ensure_ascii=False,indent=2))
print('AI core VN',len(schools),'schools',sum(len(s['items']) for s in schools),'records')
