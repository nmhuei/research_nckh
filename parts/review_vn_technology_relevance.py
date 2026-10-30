import json, pathlib, hashlib, collections
p=pathlib.Path('/home/ubuntu/university_research')
paths=[p/'parts/vn_research.json',p/'parts/vn_core_research.json',p/'bibliography_classified.json']
original_hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}
sets=[json.loads(f.read_text()) for f in paths]
vn=[{'school':s['name'],**i} for d in sets[:2] for s in d['schools'] for i in s['items']]
bib=sets[2] if isinstance(sets[2],list) else sets[2].get('items',sets[2].get('records',[]))
ptit=[i for i in bib if i.get('school')=='PTIT']
assert len(vn)==39 and len(ptit)==23
exclude_title='Đánh giá nhận thức về rủi ro an toàn giao thông trong hoạt động tìm kiếm chỗ đỗ và đỗ xe trên đường tại Hà Nội theo cách tiếp cận đa chiều'
exclude_reason='Khảo sát nhận thức và hành vi về rủi ro đỗ xe trên 485 người; dùng thống kê để mô tả vấn đề quản lý/an toàn giao thông. Tóm tắt không xác lập đóng góp về thuật toán, hệ thống số, cảm biến, thiết bị, vật liệu hoặc phương pháp thiết kế kỹ thuật. Loại theo phạm vi công nghệ chặt chẽ của yêu cầu mới.'
# Each reason was manually reviewed against title, supplied evidence/summary and,
# where needed, newly consulted primary publisher/university sources.
vn_reasons=[
'Mô hình học sâu có khả năng giải thích cho ảnh MRI và hỗ trợ chẩn đoán; đóng góp phương pháp AI/y sinh.',
'So sánh các kiến trúc phát hiện vật thể cho ảnh tế bào máu; kỹ thuật thị giác máy tính/y sinh.',
'Mô hình tương tác động lực học–nhiệt để mô phỏng phanh ô tô bằng MATLAB và Ansys; kỹ thuật cơ khí.',
'Mạng U-Net cải tiến dự báo trường dòng chảy quanh cánh máy bay; phương pháp tính toán phục vụ kỹ thuật hàng không.',
'Đánh giá quy trình chế tạo đắp dây hồ quang và CNC cho chi tiết hợp kim; trọng tâm kỹ thuật chế tạo và tác động của quy trình dù có thành phần chi phí.',
'Phát triển giao thức tính toán bảo mật cho hệ tư vấn có bảo vệ riêng tư; mật mã và hệ thống tính toán.',
'Xây dựng công cụ kiểm tra an toàn mã nguồn do LLM sinh; kỹ thuật phần mềm/an ninh mạng, dù mới xác nhận metadata đồ án.',
'Thiết kế/thử nghiệm thành phần vữa cho mặt đường và tính chất cơ lý; kỹ thuật vật liệu xây dựng.',
exclude_reason,
'Tích hợp GNSS-RTK, IoT và điện toán đám mây để quan trắc kết cấu cầu theo thời gian thực; hệ thống cảm biến kỹ thuật.',
'Chế tạo lớp phủ epoxy với hạt nano biến tính để chống ăn mòn thép; kỹ thuật vật liệu/hóa học.',
'Mô hình học tổ hợp LSTM phát hiện tấn công MITM trong ICS; thuật toán bảo mật hệ điều khiển.',
'Kiến trúc VLM gọn phân biệt bối cảnh cháy trong nhà; kỹ thuật AI/thị giác máy tính.',
'Đề tài dự kiến xây dựng mô hình AI và ứng dụng web cá nhân hóa học tập; giữ vì có sản phẩm phần mềm/mô hình kỹ thuật, không phải khảo sát giáo dục đơn thuần.',
'Phát triển Transformer cho định vị trong nhà từ WiFi fingerprinting; thuật toán AI và vô tuyến.',
'Phát triển giải pháp định vị UWB cho robot tự hành trong nhà máy; robot và điện tử/viễn thông.',
'Thiết kế/mô phỏng vật liệu hai chiều cho linh kiện trở nhớ; vật liệu và linh kiện điện tử, có ứng dụng kỹ thuật cụ thể.',
'Tổng hợp và đánh giá xúc tác điện hóa tạo hydro; ứng dụng năng lượng cụ thể, không phải nghiên cứu hóa học nền tảng không có đích công nghệ.',
'Thiết kế bộ điều khiển Fuzzy-PID và ước lượng gió ổn định UAV; điều khiển tự động.',
'Phát hiện và theo dõi phương tiện bằng phương pháp xử lý dữ liệu hình ảnh; kỹ thuật nhận dạng phục vụ giao thông.',
'Thuật toán mạng tương đồng bệnh và Random Walk with Restart để dự đoán liên hệ thuốc–bệnh; tin sinh học/tính toán y sinh.',
'Mạng thích nghi miền học sâu phân loại lưu lượng mã hóa; thuật toán AI và mạng.',
'Kết hợp học tổ hợp/mô hình ngôn ngữ lập trình để phát hiện code smell; kỹ thuật chất lượng phần mềm.',
'So sánh tinh chỉnh LLM và RAG trên dữ liệu luật tiếng Việt; đóng góp phương pháp AI dù miền ứng dụng là pháp luật.',
'Khung hỏi đáp đa tác tử với lập kế hoạch và truy xuất tri thức động; thuật toán/hệ thống AI.',
'Học tăng cường sâu cho lập lịch trên HPC; đóng góp thuật toán hệ thống tính toán, không phải quản trị chi phí đơn thuần.',
'Tinh chỉnh Sentence-BERT tạo đặc trưng dự đoán kết quả tác vụ HPC; AI và tính toán hiệu năng cao.',
'Hệ thống cảnh báo ngập tích hợp AI/GIS; kỹ thuật môi trường và hệ thống thông tin.',
'Hệ thống truy xuất đa phương thức tích hợp OCR, nhận dạng tiếng nói và CLIP; kỹ thuật tìm kiếm thông tin.',
'Đánh giá độ bền và khả năng giải thích của LLM phát hiện lỗ hổng mã; kỹ thuật an toàn phần mềm.',
'Môi trường mô phỏng roaming dữ liệu mạng 5G; phần mềm và mạng viễn thông.',
'Khung đa tác tử tự động phát hiện lỗ hổng và phát cảnh báo; an ninh mạng/AI.',
'Mô hình học máy dự báo điều kiện môi trường nhà kính; phương pháp tính toán cho nông nghiệp thông minh.',
'Thiết kế/chế tạo tay máy sáu bậc tự do tích hợp camera và AI; robot/tự động hóa.',
'Thiết kế dựa trên mô hình, mô phỏng và sinh mã cho robot cân bằng dùng PID/LQR; điều khiển và hệ nhúng.',
'Thuật toán tối ưu Walrus kết hợp học sâu dự báo nỗ lực phần mềm; giữ vì đánh giá mô hình dự đoán cụ thể, không phải quản trị dự án thuần túy.',
'Hệ phát hiện cháy kết hợp xử lý ảnh, học máy và cảm biến IoT; hệ thống kỹ thuật tích hợp.',
'Mô hình GCN theo miền kết hợp DomBert để phân tích cảm xúc; thuật toán xử lý ngôn ngữ.',
'Điều khiển dự báo phi tuyến cho bám quỹ đạo/tránh vật cản của robot; mô phỏng ROS/Gazebo và thử robot thực.'
]
ptit_reasons=[
'Học tổ hợp stacking nhiều tầng phát hiện rối loạn nhịp từ ECG; thuật toán AI/y sinh.',
'Phân tích hiệu năng hệ vô tuyến có nhiều RIS và truyền gói ngắn; kỹ thuật viễn thông.',
'Thiết kế ăng ten MIMO băng siêu rộng và cách ly cao cho 5G; điện tử/viễn thông.',
'Phát hiện nhịp tim bằng học sâu trên ECG; kỹ thuật xử lý tín hiệu y sinh.',
'Khung định vị hợp tác V2V dựa trên nhận thức; thuật toán định vị/hệ giao thông thông minh.',
'Mô hình học máy dự báo suy tim từ dữ liệu di truyền; AI/tin sinh học có mục tiêu chẩn đoán.',
'Mô hình học máy dự báo sống còn và xác định yếu tố đầu vào trong suy tim; kỹ thuật dự đoán y sinh, không chỉ nghiên cứu lâm sàng mô tả.',
'Đánh giá thực nghiệm giao thức VPN WireGuard, OpenVPN và IPsec; kỹ thuật mạng/bảo mật.',
'Lập lịch dựa trên kênh và xác suất gián đoạn trong hệ RIS-NOMA; kỹ thuật truyền thông.',
'Chiến lược chuyển giao phổ trong vô tuyến nhận thức hỗ trợ IoT; giao thức và kỹ thuật mạng.',
'Phân tích hệ truyền NOMA hợp tác dùng RIS-UAV với độ dài khối hữu hạn; kỹ thuật viễn thông.',
'Cải thiện mạng cảm biến quang FBG tích hợp DWDM; kỹ thuật quang và truyền thông.',
'PCA và học máy phân loại rối loạn nhịp từ ECG; phương pháp xử lý tín hiệu/AI.',
'Giao thức PMME thích nghi và hiệu năng mạng cảm biến đa sự kiện; kỹ thuật giao thức.',
'Thiết kế mạch RF-DC đa băng thu năng lượng cho cảm biến IoT; mạch điện tử/năng lượng.',
'Thiết kế nền tảng thực hành AIoT trực tuyến; đối tượng đóng góp là nền tảng kỹ thuật. Chỉ xác nhận tiêu đề/thư mục từ khoa và danh sách nghiên cứu chính thức; chưa đọc abstract/toàn văn.',
'Mô hình tính toán kết hợp Signature Theory và Rough Fractional Stochastic Volatility để cập nhật/dự báo dữ liệu tài chính trực tuyến; có đóng góp phương pháp tính toán rõ trong abstract, nên giữ dù ứng dụng tài chính.',
'Ứng dụng TinyML trong nông nghiệp và sản xuất; học máy trên thiết bị tài nguyên hạn chế.',
'Mô hình học máy dự báo môi trường nhà kính; kỹ thuật AI cho nông nghiệp thông minh.',
'Thiết kế/phân tích hệ thông tin quang vệ tinh kết hợp phân phối khóa lượng tử CV-QKD; truyền thông và bảo mật.',
'MIMO phi tế bào cho truyền thông vệ tinh quỹ đạo thấp; kỹ thuật viễn thông.',
'Phân tích lỗi khối với gây nhiễu hợp tác trong truyền thông bảo mật; kỹ thuật truyền thông/bảo mật.',
'Thuật toán chọn đặc trưng cho chẩn đoán ALS bằng học máy; AI/y sinh.'
]
assert len(vn_reasons)==39 and len(ptit_reasons)==23
vn_review={'keep':[i['title'] for i in vn if i['title']!=exclude_title],'exclude':[{'title':exclude_title,'reason_vi':exclude_reason}],'uncertain':[]}
ptit_review={'keep':[i['title'] for i in ptit],'exclude':[],'uncertain':[]}
for name,review,rows in [('vn_relevance_review.json',vn_review,vn),('ptit_bib_relevance.json',ptit_review,ptit)]:
 decisions=review['keep']+[r['title'] for r in review['exclude']+review['uncertain']]
 assert collections.Counter(decisions)==collections.Counter(i['title'] for i in rows)
 (p/'parts'/name).write_text(json.dumps(review,ensure_ascii=False,indent=2))
audit={'reviewed_at':'2026-10-30','scope_vi':'Rà thủ công tính phù hợp công nghệ của 39 mục nghiên cứu VN và 23 bản ghi thư mục PTIT. Đây là kiểm tra phạm vi chủ đề, không nâng mức xác minh khoa học hoặc khẳng định đã đọc toàn văn.','criteria_vi':'Giữ đóng góp kỹ thuật về thuật toán/phương pháp tính toán, phần mềm, bảo mật, điện tử, robot, vật liệu, năng lượng/môi trường kỹ thuật hoặc công nghệ y sinh. Ứng dụng kỹ thuật trong giáo dục, luật và tài chính vẫn thuộc phạm vi. Loại khảo sát hành vi/quản lý không có đóng góp kỹ thuật cụ thể.','source_files_sha256':original_hashes,'items':[],'additional_evidence':[{'title':exclude_title,'url':'https://tcsj.utc.edu.vn/index.php/tcgtvt/article/view/3056','evidence_vi':'Abstract nêu khảo sát 485 phiếu, 30 tình huống rủi ro, Cronbach alpha; trọng tâm nhận thức rủi ro đỗ xe.'},{'title':ptit[15]['title'],'url':'https://khcn.ptit.edu.vn/khcn/danh-sach-bai-bao-cong-bo-tren-cac-tap-chi-khoa-hoc-trong-nuoc-nam-2025/','evidence_vi':'Danh mục chính thức mục 173 xác nhận tên bài về thiết kế nền tảng AIoT, số 04 (CS.01) 2025, trang 88–95. Không có nội dung abstract trong trang danh mục.'},{'title':ptit[16]['title'],'url':'https://www.vjol.info.vn/3126-3445/article/view/258017/','evidence_vi':'Abstract tạp chí qua chỉ mục tìm kiếm nêu kết hợp Signature Theory và RFSV, ước lượng/cập nhật trực tuyến cho dữ liệu giá–khối lượng, thực nghiệm VN30. Mở trực tiếp trả 502; không tuyên bố đọc toàn văn. Metadata tạp chí ghi 2026 nhưng danh mục khoa ghi 2025; cần giữ ghi chú năm nguồn khác nhau.'}]}
for rows,reasons,group in [(vn,vn_reasons,'vn_research_and_core'),(ptit,ptit_reasons,'ptit_bibliography')]:
 for row,reason in zip(rows,reasons):
  audit['items'].append({'group':group,'school':row['school'],'title':row['title'],'decision':'exclude' if row['title']==exclude_title else 'keep','reason_vi':reason,'source_url':row.get('url',row.get('source_url'))})
(p/'parts/vn_technology_relevance_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
assert all(hashlib.sha256(f.read_bytes()).hexdigest()==original_hashes[str(f)] for f in paths)
print(json.dumps({'reviewed':len(audit['items']),'vn_keep':len(vn_review['keep']),'vn_exclude':len(vn_review['exclude']),'vn_uncertain':0,'ptit_keep':len(ptit_review['keep']),'ptit_exclude':0,'ptit_uncertain':0,'original_files_unchanged':True}))
