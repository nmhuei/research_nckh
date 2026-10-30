import json
from pathlib import Path
root=Path('/home/ubuntu/university_research');parts=root/'parts'
v=[x for x in json.loads((root/'bibliography_classified.json').read_text())['records'] if x['school']=='VKU']
keep={1,7,11,12,13,14,15,16,18,19,20,22,23,24,33,34,36,37,38,42,47,52,60,61,72,73,82,92,95,96,101,102,103,104,105,106,107,108,110,111}
uncertain={
27:'Tóm tắt chỉ áp dụng và so sánh GM/FGM có sẵn để dự báo hàng hóa cho quy hoạch cảng; chưa xác định được đóng góp mới về thuật toán, phần mềm hoặc hệ thống kỹ thuật. Tạm loại khỏi dữ liệu chính.',
40:'Tóm tắt chủ yếu dự báo kim ngạch xuất khẩu bằng GM/DGM có sẵn để hỗ trợ hoạch định kinh tế; chưa đủ bằng chứng về đóng góp phương pháp tính toán hoặc công nghệ. Tạm loại khỏi dữ liệu chính.',
41:'Tóm tắt nêu khung phân tích KPI cầu thủ và advanced analytics nhưng không chỉ rõ thuật toán, hệ thống hay cải tiến kỹ thuật; chưa phân biệt được nghiên cứu công nghệ với báo cáo phân tích thể thao. Tạm loại khỏi dữ liệu chính.',
57:'Tóm tắt mô tả áp dụng GM(1,1) có sẵn cho dự báo bỏ học và khuyến nghị quản lý; chưa thấy đóng góp về thuật toán, phần mềm hoặc hệ thống giáo dục thông minh. Tạm loại khỏi dữ liệu chính.',
75:'Tóm tắt áp dụng GM/DGM có sẵn để dự báo hàng hóa phục vụ chính sách và quản lý cảng; chưa đủ bằng chứng đóng góp kỹ thuật của phương pháp hay hệ thống. Tạm loại khỏi dữ liệu chính.',
91:'Tóm tắt nêu mô hình MCDM tích hợp để chọn nhà cung cấp vận tải nhưng không đủ chi tiết xác nhận cải tiến thuật toán hoặc hệ thống quyết định; có thể chỉ là ứng dụng phương pháp quản trị. Tạm loại khỏi dữ liệu chính.',
109:'Tóm tắt áp dụng GM/DGM có sẵn để dự báo hàng hóa phục vụ chính sách và quản lý cảng; chưa đủ bằng chứng đóng góp kỹ thuật của phương pháp hay hệ thống. Tạm loại khỏi dữ liệu chính.'}
reasons={}
def add(ids,reason):
 for n in ids:
  assert n not in reasons;reasons[n]=reason
add([2,62],'Nghiên cứu phương pháp giảng dạy vật lý và mức độ tham gia/sáng tạo của sinh viên; không phải nghiên cứu thiết bị, thuật toán hoặc công nghệ vật lý.')
add([3],'Nghiên cứu khung pháp luật cho hợp đồng lao động điện tử; không trình bày đóng góp công nghệ hợp đồng hay an toàn hệ thống.')
add([4,10,55,74,76,79],'Nghiên cứu ngôn ngữ hoặc sư phạm ngoại ngữ; không có dấu hiệu phát triển phương pháp xử lý ngôn ngữ bằng máy hay hệ thống công nghệ.')
add([5,21,87,93],'Nghiên cứu tài chính, chính sách hoặc kinh tế xanh/phát triển bền vững; không phải kỹ thuật năng lượng hay môi trường.')
add([6],'Đã đọc abstract: đánh giá khái niệm, lợi ích, rào cản và khuyến nghị quản trị/pháp lý cho blockchain trong tài trợ chuỗi cung ứng; không thiết kế thuật toán, giao thức hoặc hệ thống blockchain.')
add([8],'Mục giới thiệu số chuyên đề (special issue/editorial), không phải một công trình nghiên cứu công nghệ cụ thể.')
add([9],'Mô hình tổ chức giáo dục OMO và giải pháp học tập; tiêu đề không nêu thiết kế phần mềm, thuật toán hoặc hạ tầng kỹ thuật cụ thể.')
add([17,45,46,58,63,64,65,66,67,71],'Nghiên cứu hành vi, sự hài lòng, lòng trung thành hoặc yếu tố kinh tế/quản trị du lịch và dịch vụ; không phải phát triển hay đánh giá công nghệ kỹ thuật.')
add([25],'Đã đọc abstract: khảo sát nhận thức, kỳ vọng và ý định dùng tư vấn AI, kèm phân tích thang đo; không xây dựng hoặc đánh giá thuật toán/hệ thống tư vấn AI.')
add([26,28],'Nghiên cứu thương hiệu đại học và quyết định chọn trường/ngành; thuộc marketing/giáo dục, không phải công nghệ.')
add([29],'Đã đọc abstract: bàn về lợi ích, thách thức và khuyến nghị sử dụng CNTT trong tư vấn giáo dục; không có hệ thống hay phương pháp tính toán được triển khai.')
add([30],'Tổng quan trắc lượng thư mục về kế toán xanh; sử dụng công cụ phân tích tài liệu không tự tạo thành đóng góp công nghệ.')
add([31,44,69,70,85,100],'Nghiên cứu quản trị, lãnh đạo, động lực hoặc hành vi lao động/khởi nghiệp; không có đóng góp công nghệ cụ thể.')
add([32,48,94,98],'Nghiên cứu đánh giá/đào tạo/phương pháp giáo dục; không đề xuất thuật toán, hệ thống phần mềm hoặc thiết bị phục vụ giáo dục.')
add([35,53],'Nghiên cứu kinh tế, thương mại và đầu tư; không nêu đóng góp công nghệ hoặc phương pháp tính toán mới.')
add([39],'Nghiên cứu sử dụng nền tảng Padlet có sẵn để dạy tiếng Anh; thuộc sư phạm ứng dụng công cụ, không phát triển công nghệ.')
add([43,54,56],'Nghiên cứu chiến lược marketing, sử dụng công cụ quảng cáo hoặc phát triển sản phẩm du lịch; không phát triển thuật toán/hệ thống kỹ thuật.')
add([49],'Đã đọc abstract: phân tích rủi ro/thiệt hại deepfake và đưa khuyến nghị pháp lý, nhận thức, phối hợp; không thiết kế hoặc kiểm thử cơ chế phát hiện/xác thực kỹ thuật.')
add([50],'Đã đọc abstract: nghiên cứu tình huống và phản hồi người dùng về tác động AI đến trải nghiệm/mua sắm; không phát triển hệ gợi ý, mô hình AI hoặc chatbot.')
add([51],'Đã đọc abstract: tổng quan tình hình, lợi ích và rào cản chấp nhận blockchain tại doanh nghiệp logistics; đóng góp là giải pháp quản trị, không phải thuật toán/giao thức/hệ thống.')
add([59],'Đã đọc abstract: dùng AHP có sẵn trên khảo sát chuyên gia để xếp hạng yếu tố mô hình kinh doanh; đóng góp chính là quản trị khởi nghiệp, không cải tiến thuật toán AHP.')
add([68],'Đã đọc abstract: tổng quan cơ hội, thách thức, đạo đức và khung đào tạo khi sử dụng AI ở đại học; không trình bày công nghệ hay hệ thống AI cụ thể được phát triển.')
add([77,78],'Nghiên cứu chính trị, tư tưởng hoặc triết học; không liên quan đến nghiên cứu công nghệ.')
add([80],'Đã đọc abstract: dùng TAM/UTAUT nghiên cứu sự chấp nhận chatbot và trải nghiệm khách hàng; không phát triển chatbot hay thuật toán ngôn ngữ.')
add([81],'Chiến lược phát triển năng lực số trong giáo dục; thuộc chính sách/đào tạo, không nghiên cứu kỹ thuật số cụ thể.')
add([83,88],'Nghiên cứu ý định chuyển đổi số hoặc hiệu quả doanh nghiệp tài chính/kế toán; không có đóng góp thuật toán, phần mềm hoặc hệ thống.')
add([84],'Đã đọc abstract: nội dung là tổng quan ứng dụng công nghệ số, IoT và Big Data để nâng chất lượng giáo dục; không có thiết kế pipeline dữ liệu, mô hình dự đoán hoặc hệ thống được kiểm thử.')
add([86,99],'Đánh giá tác động của công cụ AI/hợp tác trực tuyến trong dạy học; không thể hiện phát triển công nghệ hay phương pháp tính toán.')
add([89,90],'Nghiên cứu hành vi mua hàng, ảnh hưởng truyền thông và mức sẵn sàng chi trả; thuộc marketing/kinh tế tiêu dùng.')
add([97],'Giải pháp tạo động lực khởi sự kinh doanh cho sinh viên; không phải công trình công nghệ.')
assert set(range(1,112))==keep|set(reasons)|set(uncertain)
assert not keep&set(reasons) and not keep&set(uncertain) and not set(reasons)&set(uncertain)
review={'keep':[x['title'] for n,x in enumerate(v,1) if n in keep], 'exclude':[{'title':v[n-1]['title'],'reason_vi':reasons[n]} for n in sorted(reasons)], 'uncertain':[{'title':v[n-1]['title'],'reason_vi':uncertain[n]} for n in sorted(uncertain)]}
(parts/'vku_bib_relevance.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
eu=json.loads((parts/'eu_research.json').read_text());eit=[x for s in eu['schools'] for x in s['items']]
eureview={'keep':[x['title'] for x in eit],'exclude':[],'uncertain':[]}
(parts/'eu_relevance_review.json').write_text(json.dumps(eureview,ensure_ascii=False,indent=2))
notes={'reviewed_on':'2026-10-30','scope_vi':'Chỉ giữ nội dung có phương pháp tính toán, thuật toán, bảo mật kỹ thuật, phần mềm, điện tử, robot, vật liệu/kỹ thuật hóa học, năng lượng/môi trường hoặc công nghệ y sinh cụ thể. Không coi một bài nghiên cứu là công nghệ chỉ vì dùng công cụ số, thống kê khảo sát, hoặc nhắc AI/blockchain. Uncertain phải loại khỏi bản dữ liệu chính.','eu_counts':{k:len(v) for k,v in eureview.items()},'vku_counts':{k:len(v) for k,v in review.items()},'evidence_vi':'Đã rà soát toàn bộ 28 mục EU với tóm tắt/nguồn chính thức đã đọc ở lượt trước; toàn bộ 111 tiêu đề VKU và 25 abstract bổ sung từ elib.vku.udn.vn. Không đọc toàn văn các mục VKU có yêu cầu đăng nhập.','vku_abstract_evidence_file':str(root/'raw/europe/vku_relevance_evidence.json'),'eu_borderline_keep_reasons_vi':{'technoeconomic_perovskite':'Có mô hình quá trình sản xuất từ dưới lên, xét vật liệu, kỹ thuật chế tạo và mức tự động hóa; là đánh giá kỹ thuật-kinh tế công nghệ năng lượng, không phải kinh tế thuần túy.','hydrogen_transport_assessment':'Phân tích chuỗi chuyển đổi, lưu trữ, hóa lỏng/khí hóa và hoàn nguyên các chất mang hydro với hiệu suất năng lượng; có nội dung kỹ thuật quá trình cụ thể.','hydrogen_supply_chain_review':'Tổng quan kỹ thuật có phân tích độ tinh khiết và công nghệ chuỗi cung ứng hydro; giữ dưới loại review_article.','robot_collaboration_scale':'Đánh giá năng lực của hệ robot qua nhận biết tình huống, thích nghi, giao tiếp, học và di chuyển; đối tượng và chỉ tiêu là kỹ thuật robot, không phải quản trị nhân sự.','quantum_devices_and_clock':'Có bộ làm lạnh mạch lượng tử, máy đo phổ nhiệt trên chip và đồng hồ hạt nhân có vòng phản hồi được thực nghiệm; không phải vật lý thuần túy không ứng dụng.'},'vku_kept_borderline_indices':[11,15,22,61,72,73,95,103,110],'vku_uncertain_indices':sorted(uncertain),'original_files_edited':False}
(parts/'strict_relevance_review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print(json.dumps({'EU':notes['eu_counts'],'VKU':notes['vku_counts'],'all_input_titles_partitioned':True},ensure_ascii=False,indent=2))
