import json
from config import ROOT, DATE, TOPICS

schools=[]
def school(name,domain,portals):
 s={'name':name,'domain':domain,'country_code':'VN','country':'Viet Nam','website':'https://'+domain+'/',
 'research_portals':[{'title':t,'url':u} for t,u in portals],'items':[]};schools.append(s);return s
def item(s,title,year,kind,codes,summary,url,doi=None,note='Đã đọc metadata và tóm tắt; chưa đọc toàn văn.',sources=None):
 s['items'].append({'title':title,'year':year,'type':kind,'topic_codes':codes,'primary_topic_code':codes[0],
 'topics':[TOPICS[c][0] for c in codes],'summary_vi':summary,'url':url,'doi':doi,
 'source_urls':list(dict.fromkeys([url]+(sources or []))),'verification_note':note,
 'full_text_read':False,'checked_on':DATE,'classification_method':'Phân loại thủ công theo nguồn đã đọc; nhiều nhãn khi liên ngành.'})

udte='https://usth.edu.vn/en/publications-of-department-of-technology-and-engineering-4274/'
ucet='https://usth.edu.vn/en/publications-4442/'
s=school('Trường Đại học Khoa học và Công nghệ Hà Nội (USTH)','usth.edu.vn',[('Công bố Khoa Công nghệ và Kỹ thuật',udte),('Công bố Khoa Công nghệ Hóa học và Môi trường',ucet)])
item(s,'Synthesis of an imine-type nickel complex and investigation of its electrocatalytic activity for H2 evolution',2025,'journal_article',['ENERGY','MATERIALS'],
 'Tổng hợp phức nickel và khảo sát xúc tác điện hóa tạo hydro. Nguồn mô tả thí nghiệm điện hóa và phân tích cơ chế; đây là nghiên cứu xúc tác ở quy mô phòng thí nghiệm.',
 'https://pubs.rsc.org/en/content/articlelanding/2025/ra/d4ra08116a','10.1039/D4RA08116A',sources=[ucet])
item(s,'Design and Development of a Fuzzy-PID Controller with Integrated Wind Estimation for UAV Hexacopter Stabilization',2025,'journal_article',['ROBOTICS','CONSTRUCTION_TRANSPORT'],
 'Bộ điều khiển Fuzzy-PID tích hợp ước lượng gió để ổn định UAV sáu cánh. Chủ đề được xác định từ tiêu đề công bố, chưa đủ dữ liệu để kết luận hiệu quả thực nghiệm.',udte,
 note='Đã đọc danh mục công bố chính thức của khoa; tạp chí Journal of Aeronautics, Astronautics and Aviation 57(5),1281–1289. Chưa đọc abstract/toàn văn; chưa tìm được DOI.')
item(s,'Vehicle Detection and Tracking in Vietnam’s Complex Urban Traffic',2025,'conference_paper',['AI_DATA','CONSTRUCTION_TRANSPORT'],
 'Phát hiện và theo dõi phương tiện trong giao thông đô thị Việt Nam. Chưa xác minh bộ dữ liệu hoặc chỉ số đánh giá vì nguồn đang là thông tin thư mục.',udte,
 note='Danh mục chính thức ghi Advances in Information and Communication Technology, trang529–538, ISBN978-3-031-80943-9; chưa đọc abstract/toàn văn.')

hs='https://soict.hust.edu.vn/en/2025-publications.html'
s=school('Đại học Bách khoa Hà Nội (HUST)','hust.edu.vn',[('Nghiên cứu HUST','https://www.hust.edu.vn/vi/nghien-cuu/'),('Công bố SoICT năm2025',hs)])
item(s,'Improving computational drug repositioning through multi-source disease similarity networks',2025,'journal_article',['BIOTECH_HEALTH','COMPUTING'],
 'Kết hợp mạng tương đồng bệnh từ kiểu hình, ontology và dữ liệu phân tử, dùng Random Walk with Restart để dự đoán liên hệ thuốc–bệnh. Mục tiêu là tìm ứng dụng mới của thuốc; chưa phải bằng chứng hiệu quả điều trị.',
 'https://www.nature.com/articles/s41598-025-04772-0','10.1038/s41598-025-04772-0',
 note='Đã đọc abstract và mô tả phương pháp; xác nhận đơn vị HUST qua thông tin tác giả/PubMed. Chưa thẩm định toàn văn hoặc tái lập.',sources=[hs,'https://pubmed.ncbi.nlm.nih.gov/40841559/'])
item(s,'Encrypted Traffic Classification Through Deep Domain Adaptation Network With Smooth Characteristic Function',2025,'journal_article',['CYBERSECURITY','AI_DATA'],
 'Phân loại lưu lượng mã hóa bằng mạng thích nghi miền học sâu. Hướng ứng dụng thuộc phân tích lưu lượng và an ninh mạng; chưa xác minh dữ liệu thực nghiệm.',
 'https://ieeexplore.ieee.org/document/10855613',note='Tên/năm/tạp chí được xác nhận từ danh mục SoICT; chưa đọc abstract hay toàn văn IEEE; không suy đoán DOI.',sources=[hs])
item(s,'EnseSmells: Deep ensemble and programming language models for automated code smells detection',2025,'journal_article',['COMPUTING','AI_DATA'],
 'Kết hợp học tổ hợp và mô hình ngôn ngữ lập trình nhằm phát hiện code smell trong mã nguồn. Phân loại chất lượng phần mềm và AI dựa theo tiêu đề thư mục.',
 'https://www.sciencedirect.com/science/article/pii/S0164121225000433',note='Danh mục SoICT2025 xác nhận tên và Journal of Systems and Software; chưa đọc nội dung nhà xuất bản.',sources=[hs])

uet='https://uet.vnu.edu.vn/~cuongnv/'
s=school('Trường Đại học Công nghệ – ĐHQG Hà Nội (UET)','uet.vnu.edu.vn',[('Trang nghiên cứu và công bố Nguyễn Việt Cường',uet)])
item(s,'Adapting Large Language Models to Vietnamese Law: Pretrained LLM Refinement vs Retrieval Augmented Generation',2024,'conference_paper',['AI_DATA','COMPUTING'],
 'So sánh tinh chỉnh mô hình ngôn ngữ và truy xuất tăng cường cho dữ liệu luật tiếng Việt. Không rút ra mô hình tốt hơn vì chưa đọc phần thực nghiệm.',
 'https://doi.org/10.1109/KSE63888.2024.11063566','10.1109/KSE63888.2024.11063566',
 note='Trang giảng viên UET liệt kê bài KSE2024 và DOI; IEEE yêu cầu JavaScript. Quy thuộc qua danh mục giảng viên, chưa đối chiếu toàn bộ affiliation của bài.',sources=[uet])
item(s,'PRADA-QA: Product QA with Multi-Agent Planning and Dynamic Knowledge Retrieval',2025,'conference_paper',['AI_DATA','COMPUTING'],
 'Hỏi đáp sản phẩm bằng lập kế hoạch đa tác tử và truy xuất tri thức động. Chủ đề dựa trên tiêu đề công bố, chưa có đánh giá nội dung đầy đủ.',
 'https://doi.org/10.1007/978-981-92-2590-3_24','10.1007/978-981-92-2590-3_24',
 note='Danh mục giảng viên UET ghi SOICT2025, CCIS2914,trang287–302. 2025 là năm hội nghị theo danh mục; chưa xác minh năm phát hành kỷ yếu. Chưa đọc abstract/toàn văn.',sources=[uet])

hpub='https://hpcc.hcmut.edu.vn/publications';hresearch='https://hpcc.hcmut.edu.vn/research'
s=school('Trường Đại học Bách khoa – ĐHQG TP.HCM (HCMUT)','hcmut.edu.vn',[('Nghiên cứu HPCC',hresearch),('Công bố HPCC',hpub),('Công bố Địa chất–Dầu khí','https://geopet.hcmut.edu.vn/en/nghien-cuu/cong-bo-khoa-hoc?year=2025')])
item(s,'Toward Sustainable and Cost-Efficient HPC Systems: A Deep Reinforcement Learning Job Scheduling Approach',2025,'book_chapter',['COMPUTING','AI_DATA','ENERGY'],
 'Ứng dụng học tăng cường sâu cho lập lịch tác vụ trên hệ thống tính toán hiệu năng cao, hướng đến hiệu quả chi phí và tính bền vững.',hpub,
 note='HPCC ghi năm2025, Lecture Notes in Computer Science16354,trang409–420. Đã đọc thông tin thư mục và nhãn chủ đề của phòng thí nghiệm; chưa đọc abstract/toàn văn.')
item(s,'Fine-Tuned Sentence-BERT for HPC Job Outcome Prediction via Textual Feature Embedding',2026,'conference_paper',['COMPUTING','AI_DATA'],
 'Dự đoán kết quả tác vụ HPC bằng đặc trưng văn bản từ Sentence-BERT đã tinh chỉnh. Chưa xác minh tập dữ liệu và kết quả định lượng.',hpub,
 note='HPCC ghi SCA/HPCAsia2026 Workshops, ACM; xác nhận từ danh mục công bố phòng thí nghiệm, chưa đọc abstract/toàn văn.')
item(s,'AI- and GIS-based Flood Warning System for Ho Chi Minh City',None,'institutional_research_project',['ENVIRONMENT','AI_DATA'],
 'Dự án kết hợp AI và GIS cho cảnh báo ngập tại TP.HCM. Trang HPCC đánh dấu đã hoàn thành nhưng trang tổng quan không nêu năm triển khai.',hresearch,
 note='Đã đọc phần mô tả dự án của phòng thí nghiệm; không coi đây là tên một bài báo hoặc suy ra năm từ thời điểm truy cập.')

uit1='https://www.uit.edu.vn/bai-viet/chuc-mung-nhom-sinh-vien-uit-co-bai-bao-khoa-hoc-duoc-cong-bo-tai-hoi-nghi-quoc-te-soict-2025'
uit2='https://www.uit.edu.vn/bai-viet/cong-tac-vien-uit-nghien-cuu-ket-hop-llm-va-xai-trong-phat-hien-dien-giai-va-xac-thuc-lo-hong-phan-mem'
s=school('Trường Đại học Công nghệ Thông tin – ĐHQG TP.HCM (UIT)','uit.edu.vn',[('Phòng ĐTSĐH & KHCN','https://khcn.uit.edu.vn/'),('Công bố và tin nghiên cứu UIT',uit1)])
item(s,'Fusurge: An Accelerated Query-Driven System for Multimodal Information Retrieval',2025,'conference_paper',['AI_DATA','COMPUTING'],
 'Hệ thống tìm kiếm video đa phương thức kết hợp lấy khung hình, OCR, nhận dạng tiếng nói, bộ mã hóa CLIP và xếp hạng lại theo tương tác người dùng.',uit1,
 note='Đã đọc abstract được UIT đăng kèm danh sách tác giả/sinh viên. Hội nghị SOICT2025, bản tin05/01/2026. Chưa đối chiếu kỷ yếu/DOI; chưa đọc toàn văn.')
item(s,'From Prediction to Understanding: A Robustness and Explainability Study of LLM-Based Vulnerability Detection',2026,'accepted_conference_paper',['CYBERSECURITY','AI_DATA'],
 'Đánh giá khả năng phát hiện lỗ hổng và độ ổn định của giải thích khi mã nguồn bị viết lại. Nguồn mô tả đánh giá sáu mô hình trên C/C++ và Java.',uit2,
 note='Bản tinUIT10/10/2026 nói đã được chấp nhận tại ICPADS2026; chưa xác nhận xuất bản kỷ yếu. Đã đọc tóm tắt, chưa đọc toàn văn.')

pt='https://udu.ptit.edu.vn/chuc-mung-sinh-vien-chuong-trinh-cong-nghe-thong-tin-dinh-huong-ung-dung-ptit-co-bai-bao-khoa-hoc-duoc-chap-nhan-tai-hoi-thao-nam-2025/'
ptel='https://tel.ptit.edu.vn/nghien-cuu/bai-bao-tap-chi-trong-nuoc/'
s=school('Học viện Công nghệ Bưu chính Viễn thông (PTIT)','ptit.edu.vn',[('Công bố Khoa Viễn thông1',ptel),('Dự án Khoa Viễn thông1','https://tel.ptit.edu.vn/nghien-cuu/du-an-khoa-hoc/')])
item(s,'Proposed Data Roaming Network Simulation Environment for 5G Network',2025,'accepted_conference_paper',['ELECTRONICS_TELECOM','COMPUTING'],
 'Xây dựng môi trường mô phỏng roaming dữ liệu trên mạng5G, phục vụ phân tích độ trễ, hiệu năng và các kịch bản chuyển vùng.',pt,
 note='PTIT đăng26/02/2026 về bài được chấp nhận ở hội thảo2025. Đã đọc mô tả công trình, chưa có DOI hay xác nhận bản kỷ yếu cuối cùng.')
item(s,'AUTOGENT: Multi-Agent AI Framework for Automated Vulnerability Detection and Security Alerting in Networked Systems',2025,'accepted_conference_paper',['CYBERSECURITY','AI_DATA'],
 'Khung AI đa tác tử cho thu thập dữ liệu, phát hiện lỗ hổng và tạo cảnh báo an ninh mạng. Nguồn là bản tin nghiên cứu của chương trình UDU.',pt,
 note='Bản tin chính thức xác nhận tác giả và người hướng dẫn; loại ghi nhận là bài đã được chấp nhận, chưa xác minh DOI/xuất bản chính thức.')
item(s,'Toward Smart Greenhouses Machine Learning Models in Environmental Status Forecast',2025,'journal_article',['AGRI_FOOD','AI_DATA','ENVIRONMENT'],
 'Dự báo trạng thái môi trường nhà kính bằng mô hình học máy. Chủ đề suy ra từ tiêu đề được khoa đưa trong danh mục công bố.',ptel,
 note='Danh mục Khoa Viễn thông1 ghi tác giảNguyễn Thanh Trà, năm2025, JSTIC/PTIT. Chưa đọc abstract/toàn văn, chưa tìm được DOI.')

s=school('Trường Đại học Bách khoa – Đại học Đà Nẵng (DUT)','dut.udn.vn',[('Phòng KHCN và HTQT','https://dut.udn.vn/Phong/Khoahoc'),('Danh mục công bố2025–2026','https://dut.udn.vn/Phong/Khoahoc/Thongbao/id/12140')])
item(s,'Design and implementation of an AI-integrated 6-DOF robotic arm for automated package and orientation recognition',2025,'journal_article',['ROBOTICS','AI_DATA'],
 'Thiết kế tay máy sáu bậc tự do với hai camera để nhận dạng bao gói và tư thế lon trên băng chuyền. Abstract có mô tả chế tạo, hệ truyền động và thử nghiệm nhận dạng.',
 'https://jst-ud.vn/jst-ud/article/view/10204','10.31130/ud-jst.2025.23(9D).555E',note='Đã đọc abstract và affiliation: ba tác giảDUT, một tác giảChungnam. Xuất bản30/09/2025; chưa đọc toàn văn.')
item(s,'Model-based design of a ballbot system controlled by mindstorms EV3',2026,'journal_article',['ROBOTICS','COMPUTING'],
 'Triển khai quy trình thiết kế dựa trên mô hình: nhận dạng hệ, mô phỏng MATLAB/Simulink và sinh mã cho LEGO EV3. Điều khiển PID cho động cơ và LQR để giữ cân bằng Ballbot.',
 'https://jst-ud.vn/jst-ud/article/view/10268','10.31130/ud-jst.2026.24(1).617E',note='Đã đọc abstract, affiliation và ngày xuất bản28/02/2026 trên trang tạp chí; chưa đọc toàn văn.')

s=school('Trường Đại học CNTT và Truyền thông Việt–Hàn (VKU)','vku.udn.vn',[('Kho tài nguyên số VKU','https://elib.vku.udn.vn/community-list?locale=vi'),('Bài báo2025','https://elib.vku.udn.vn/handle/123456789/5064')])
item(s,'An Experimental Study of Walrus Optimization-Based Deep Learning Models for Software Effort Estimation',2025,'conference_paper',['COMPUTING','AI_DATA'],
 'Kết hợp thuật toán tối ưu Walrus với các mô hình học sâu để ước lượng nỗ lực phát triển phần mềm. Abstract nêu đánh giá trên năm bộ dữ liệu SEE và nhiều thước đo sai số.',
 'https://elib.vku.udn.vn/handle/123456789/7683','10.1109/RIVF68649.2025.11365197',note='Đã đọc metadata/abstract ở bộ sưu tập bài báoVKU, RIVF2025. Toàn văn yêu cầu đăng nhập; quy thuộc theo kho cơ quan, chưa đối chiếu từng affiliation.')
item(s,'A Multimodal ML-based Indoor Fire Detection and Alarm System Using Image Processing and IoT–based Environmental Sensing',2025,'conference_paper',['ELECTRONICS_TELECOM','AI_DATA'],
 'Kết hợp camera và cảm biến môi trường để nhận diện cháy, giảm báo động giả. Kết quả từ hai mô hình được đối chiếu; trường hợp không thống nhất cần người dùng xác nhận.',
 'https://elib.vku.udn.vn/handle/123456789/7663','10.1109/ATC67618.2025.11268781',note='Đã đọc metadata/abstract ở khoVKU, ATC2025; toàn văn yêu cầu đăng nhập. Không suy ra độ chính xác cụ thể từ nhận xét định tính trong abstract.')

hcv='https://fit.hcmute.edu.vn/Resources/Docs/SubDomain/fit/2025/HCMUTE_SCIENTIFIC_CV_TranQuangKhai.pdf'
s=school('Trường Đại học Công nghệ Kỹ thuật TP.HCM (HCMUTE; tên cũ Sư phạm Kỹ thuật)','hcmute.edu.vn',[('Khoa CNTT','https://fit.hcmute.edu.vn/'),('Danh mục công bố giảng viên Trần Quang Khải',hcv)])
item(s,'Domain-Oriented GCN Method for Sentiment Analysis',2025,'conference_paper',['AI_DATA','COMPUTING'],
 'Phân tích cảm xúc bằng mạng tích chập đồ thị có xét miền dữ liệu. Chủ đề được xác định từ tên công bố trong lý lịch khoa học giảng viên.',
 'https://doi.org/10.1007/978-981-96-6005-6_29','10.1007/978-981-96-6005-6_29',note='Đọc CV trên websiteKhoa CNTT: tác giảHT Phan,QK Tran,NT Nguyen, ACIIDS2025,trang408–419. Chưa đọc abstract/toàn văn.',sources=[hcv])
item(s,'Nonlinear model predictive control for trajectory tracking and dynamic obstacle avoidance in differential-drive mobile robots',2026,'journal_article',['ROBOTICS'],
 'Điều khiển dự báo phi tuyến cho robot hai bánh: ràng buộc vận tốc và khoảng cách an toàn, mô phỏng Gazebo/ROS và thử nghiệm robot thực, đối chiếu phương pháp DWA.',
 'https://ctujsvn.ctu.edu.vn/index.php/ctujsvn/article/inPress/8547','10.22144/ctujos.2026.075',note='Đã đọc abstract, tác giả và metadata; tác giả liên hệ và sinh viên có địa chỉ thuộcHCMUTE. Trang ghi xuất bản22/05/2026 nhưng URL inPress; giữ thông tin theo metadata, chưa đọc toàn văn.')

(ROOT/'parts/vn_core_research.json').write_text(json.dumps({'checked_on':DATE,'schools':schools},ensure_ascii=False,indent=2))
print('schools',len(schools),'items',sum(len(s['items']) for s in schools))
