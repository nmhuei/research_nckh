import json,pathlib
p=pathlib.Path('/home/ubuntu/university_research')
d=json.loads((p/'deliverables/research_classified.json').read_text())
plans={
'USTH':([
'Chế tạo xúc tác điện hóa từ phức nickel để tạo hydro.',
'Ổn định UAV sáu cánh bằng điều khiển Fuzzy-PID kết hợp ước lượng gió.',
'Phát hiện và theo dõi phương tiện trong giao thông đô thị Việt Nam.'
],['Lựa chọn cấu trúc xúc tác có hoạt tính tạo hydro phù hợp.','Giữ ổn định UAV khi có gió và theo dõi phương tiện trong giao thông phức tạp.'],[[0],[1],[2]]),
'HUST':([
'Dự đoán ứng dụng mới của thuốc bằng mạng tương đồng bệnh từ nhiều nguồn dữ liệu.',
'Phân loại lưu lượng mạng mã hóa bằng học sâu thích nghi miền.',
'Tự động phát hiện dấu hiệu thiết kế mã nguồn kém bằng học tổ hợp và mô hình ngôn ngữ lập trình.'
],['Kết hợp dữ liệu kiểu hình và phân tử để dự đoán liên hệ thuốc–bệnh.','Học biểu diễn lưu lượng/mã nguồn để phân loại và phát hiện vấn đề phần mềm.'],[[0],[1],[2]]),
'UET':([
'Thích nghi mô hình ngôn ngữ lớn với dữ liệu pháp luật tiếng Việt.',
'So sánh tinh chỉnh mô hình với truy xuất tăng cường RAG cho tác vụ chuyên ngành.',
'Hỏi đáp sản phẩm bằng nhiều tác tử, lập kế hoạch và truy xuất tri thức động.'
],['Lựa chọn cách bổ sung kiến thức pháp luật cho LLM.','Chia câu hỏi phức tạp thành bước truy xuất cơ sở dữ liệu, lịch sử hỏi đáp và web.'],[[0],[0],[1]]),
'HCMUT':([
'Lập lịch tác vụ HPC bằng học tăng cường sâu, xét chi phí và tính bền vững.',
'Dự đoán kết quả tác vụ HPC từ đặc trưng văn bản bằng Sentence-BERT.',
'Kết hợp AI và GIS để xây dựng hệ thống cảnh báo ngập đô thị.'
],['Phân bổ tài nguyên tính toán cho tác vụ và dự báo kết quả trước khi thực thi.','Khai thác dữ liệu không gian và AI cho cảnh báo ngập tại TP.HCM.'],[[0],[1],[2]]),
'UIT':([
'Truy xuất video đa phương thức bằng kết hợp hình ảnh, chữ và tiếng nói.',
'Tìm kiếm theo câu hỏi với mã hóa CLIP và xếp hạng lại dựa trên tương tác.',
'Đánh giá độ ổn định và khả năng giải thích của LLM phát hiện lỗ hổng phần mềm.'
],['Tìm đúng đoạn video từ nhiều loại tín hiệu và yêu cầu người dùng.','Kiểm tra kết luận và giải thích phát hiện lỗ hổng khi mã nguồn bị viết lại.'],[[0],[0],[1]]),
'PTIT':([
'Mô phỏng chuyển vùng dữ liệu trong mạng 5G để phân tích độ trễ và hiệu năng.',
'Tự động phát hiện lỗ hổng và cảnh báo an ninh mạng bằng hệ AI đa tác tử.',
'Dự báo trạng thái môi trường nhà kính bằng học máy.'
],['Tái hiện và đánh giá các kịch bản roaming 5G.','Phối hợp thu thập dữ liệu, phát hiện lỗ hổng và tạo cảnh báo tự động.'],[[0],[1],[2]]),
'DUT':([
'Thiết kế tay máy sáu bậc tự do tích hợp AI để nhận dạng bao gói và tư thế vật thể.',
'Kết hợp camera với truyền động robot cho thao tác trên băng chuyền.',
'Thiết kế robot Ballbot theo mô hình, dùng PID/LQR và sinh mã cho bộ điều khiển.'
],['Nhận biết loại vật thể và hướng đặt để robot xử lý đúng.', 'Giữ cân bằng robot qua nhận dạng hệ, mô phỏng và triển khai điều khiển.'],[[0],[0],[1]]),
'VKU':([
'Ước lượng nỗ lực phát triển phần mềm bằng học sâu kết hợp tối ưu Walrus.',
'Phát hiện cháy trong nhà từ camera và cảm biến môi trường IoT.',
'Hợp nhất kết quả nhận dạng đa phương thức để giảm báo động cháy giả.'
],['Tối ưu mô hình dự báo nỗ lực phần mềm và đánh giá sai số trên nhiều bộ dữ liệu.','Xử lý trường hợp tín hiệu hình ảnh và cảm biến đưa ra kết luận khác nhau.'],[[0],[1],[1]]),
'HCMUTE':([
'Phân tích cảm xúc theo miền bằng biểu diễn DomBert và mạng tích chập đồ thị.',
'Kết hợp các bộ phân loại theo miền để tổng hợp quyết định phân tích cảm xúc.',
'Điều khiển dự báo phi tuyến cho robot di động bám quỹ đạo và tránh vật cản động.'
],['Trích xuất đặc trưng ngôn ngữ phù hợp với từng miền dữ liệu.','Giữ robot trong giới hạn vận tốc và khoảng cách an toàn khi di chuyển.'],[[0],[0],[1]]),
'VLUTE':([
'AI có thể giải thích hỗ trợ nhận diện Alzheimer từ ảnh MRI.',
'Phát hiện và phân loại tế bào máu bằng Faster R-CNN, RetinaNet và YOLO.',
'Mô phỏng tương tác giữa động lực học phanh và nhiệt của phanh đĩa ô tô.'
],['Giải thích các vùng ảnh tác động đến dự đoán bệnh của mô hình học sâu.','So sánh khả năng nhận dạng nhiều loại tế bào và mô phỏng sự thay đổi nhiệt khi phanh.'],[[0],[1],[2]]),
'MTA':([
'Dự đoán trường áp suất và vận tốc quanh cánh máy bay bằng mạng U-Net.',
'Chế tạo chi tiết hợp kim nickel bằng đắp dây hồ quang kết hợp gia công CNC.',
'Đánh giá vòng đời và chi phí của các phương án chế tạo chi tiết hợp kim.'
],['Học ánh xạ từ hình học/bối cảnh dòng chảy đến trường dòng quanh vật thể.','So sánh quy trình đắp vật liệu–CNC với chỉ gia công CNC về tài nguyên và chi phí.'],[[0],[1],[1]]),
'KMA':([
'Phát triển giao thức tính toán bảo mật trên dữ liệu phân tán.',
'Xây dựng hệ tư vấn người dùng có bảo vệ dữ liệu riêng tư.',
'Phát triển công cụ kiểm tra an toàn mã nguồn do LLM sinh.'
],['Cân bằng tính đúng đắn, riêng tư và hiệu quả khi tính toán hệ gợi ý.','Phát hiện vấn đề bảo mật trong mã được AI tạo ra.'],[[0],[0],[1]]),
'UTC':([
'Chế tạo vữa rót giữ nước từ xỉ lò cao, tro bay và vôi cho mặt đường bán mềm.',
'Khảo sát tác động của tỷ lệ nước/bột xỉ đến độ chảy và khả năng hút nước của vữa.',
'Đánh giá cường độ và tính chất cơ lý của vật liệu mặt đường dùng phụ phẩm công nghiệp.'
],['Chọn thành phần vữa đáp ứng đồng thời khả năng thi công, giữ nước và cường độ.'],[[0],[0],[0]]),
'HUMG':([
'Quan trắc dao động cầu dây văng theo thời gian thực bằng GNSS-RTK và IoT.',
'Tích hợp dữ liệu cảm biến công trình với nền tảng điện toán đám mây.',
'Chế tạo sơn epoxy chứa nano silica biến tính để chống ăn mòn thép.'
],['Theo dõi dao động công trình từ dữ liệu đo được truyền và xử lý trực tuyến.','Tăng khả năng bảo vệ thép trong môi trường có clorua bằng phụ gia nano.'],[[0],[0],[1]]),
'HUCE':([
'Phát hiện tấn công xen giữa trong mạng điều khiển công nghiệp bằng học tổ hợp LSTM.',
'Mô phỏng hệ ICS sử dụng SDN để đánh giá cơ chế phát hiện tấn công.',
'Phân loại bối cảnh cháy trong nhà bằng mô hình ngôn ngữ–thị giác gọn.'
],['Nhận biết tấn công MITM trong lưu lượng của hệ thống điều khiển.','Phân biệt lửa được kiểm soát với cháy nguy hiểm bằng ngữ cảnh ảnh và ngữ nghĩa.'],[[0],[0],[1]]),
'FPT':([
'Phát triển mô hình AI/học máy để cá nhân hóa trải nghiệm học tập.',
'Xây dựng ứng dụng web tích hợp mô hình cá nhân hóa học tập.',
'Định vị trong nhà bằng Transformer trên dấu vân tay tín hiệu WiFi.'
],['Chuyển đầu ra mô hình cá nhân hóa thành chức năng hỗ trợ học tập.', 'Ước lượng vị trí từ đặc trưng cường độ/tín hiệu WiFi.'],[[0],[0],[1]]),
'Phenikaa':([
'Phát triển giải pháp định vị UWB cho robot di động tự hành trong nhà máy.',
'Tích hợp kỹ thuật định vị với ứng dụng robot trong sản xuất thông minh.',
'Thiết kế và mô phỏng vật liệu boron nitride hai chiều cho linh kiện trở nhớ.'
],['Xác định vị trí robot tự hành trong môi trường nhà máy.','Khảo sát cấu trúc vật liệu hai chiều phù hợp cho ứng dụng memristor.'],[[0],[0],[1]])
}
out={'retrieved_at':'2026-10-30','methodology_vi':'Các hướng cụ thể được diễn đạt từ 38 công trình đã qua lọc công nghệ. Một công trình có thể cho nhiều khía cạnh kỹ thuật; không coi đó là các nhóm nghiên cứu độc lập. Vấn đề nghiên cứu là diễn giải của người tổng hợp, không khẳng định kết quả hoặc toàn bộ chiến lược của trường. Các tuyên bố cấp trường/đơn vị được kiểm tra bổ sung và ghi riêng.','schools':[]}
for s in d['schools']:
 if s.get('country_code')!='VN':continue
 short=s['short_name'];directions,problems,idx=plans[short]
 urls=list(dict.fromkeys(i['url'] for i in s['items']))
 n=len(s['items'])
 note=f'Rút ra từ {n} công trình trong mẫu đã thu thập; không đại diện toàn bộ hướng hoặc ưu tiên nghiên cứu của trường. Các hướng có thể là những khía cạnh của cùng một công trình.'
 if short=='UTC':note+=' Cả ba hướng đều từ một bài vật liệu mặt đường; bài không đánh giá hiệu quả làm mát thực tế.'
 if short=='VLUTE':note+=' Quan hệ của tác giả với VLUTE hiện được hỗ trợ bởi email trên trang tạp chí; chưa kiểm tra affiliation toàn văn.'
 if short in ['FPT','Phenikaa']:note+=' Đây là mục tiêu đề tài được công bố; chưa coi là kết quả hoàn thành.'
 if short=='HCMUT':note+=' Mẫu tập trung vào HPCC, không đại diện tất cả các khoa của HCMUT.'
 if short=='KMA':note+=' Mục kiểm tra mã LLM là đồ án sinh viên mới kiểm tra metadata; không nâng thành ưu tiên cấp học viện.'
 rec={'short_name':short,'domain':s['domain'],'directions_vi':directions,'problems_vi':problems,'scope':'sample_based','source_urls':urls,'scope_note_vi':note,'sample_record_ids':[i['record_id'] for i in s['items']],'direction_evidence':[{'direction_vi':direction,'record_ids':[s['items'][j]['record_id'] for j in js],'source_urls':list(dict.fromkeys(s['items'][j]['url'] for j in js))} for direction,js in zip(directions,idx)]}
 if short=='HUST':
  rec['official_overview']={'scope':'official_institution_overview_verified','level':'whole_university','priorities_vi':['AI và công nghệ dữ liệu','Công nghệ sức khỏe','Vật liệu mới','Năng lượng và môi trường bền vững','Hệ thống thông minh'],'source_url':'https://www.hust.edu.vn/vi/nghien-cuu/','verification_note_vi':'Trang nghiên cứu chính thức nêu năm lĩnh vực ưu tiên. Đọc nội dung được công cụ tìm kiếm lập chỉ mục; mở trực tiếp trong lượt này trả 502. Đây là định hướng cấp đại học, tách biệt ba hướng cụ thể rút ra từ mẫu.'}
  rec['source_urls'].append(rec['official_overview']['source_url'])
 if short=='HCMUT':
  rec['official_unit_overview']={'level':'HPCC research laboratory, not whole university','directions_vi':['Hệ tính toán hiệu năng cao cho AI và ứng dụng khoa học','Nền tảng dữ liệu dòng cho IoT và dữ liệu lớn','Phương pháp lượng tử và hệ tính toán dựa trên tác tử'],'source_url':'https://hpcc.hcmut.edu.vn/research','verification_note_vi':'Đã đọc ba Research Pillars do HPCC công bố; chỉ áp dụng cho phòng thí nghiệm này.'}
  if rec['official_unit_overview']['source_url'] not in rec['source_urls']:rec['source_urls'].append(rec['official_unit_overview']['source_url'])
 out['schools'].append(rec)
assert len(out['schools'])==17
assert all(3<=len(s['directions_vi'])<=5 and 1<=len(s['problems_vi'])<=3 for s in out['schools'])
assert all(s['source_urls'] and len(s['directions_vi'])==len(s['direction_evidence']) for s in out['schools'])
(p/'parts/vn_research_directions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'schools':len(out['schools']),'directions':sum(len(s['directions_vi']) for s in out['schools']),'problems':sum(len(s['problems_vi']) for s in out['schools']),'official_university_overviews':1,'official_lab_overviews':1,'sample_items':sum(len(s['sample_record_ids']) for s in out['schools'])}))
