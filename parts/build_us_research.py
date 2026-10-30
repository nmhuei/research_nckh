import json
import sys
from pathlib import Path

TOPICS = {
    'ai_data': 'AI và dữ liệu',
    'security': 'An toàn thông tin',
    'electronics_telecom': 'Điện tử và viễn thông',
    'robotics': 'Robot và tự động hóa',
    'materials': 'Vật liệu và chế tạo',
    'energy': 'Năng lượng',
    'environment': 'Môi trường và phát triển bền vững',
    'biotech': 'Công nghệ sinh học và y sinh',
    'construction_transport': 'Xây dựng và giao thông',
    'basic_science': 'Khoa học cơ bản',
}

schools = []

def school(name, domain, portals):
    out = {'name': name, 'country': 'United States', 'country_code': 'US',
           'domain': domain, 'website': 'https://www.' + domain + '/',
           'research_portals': [{'title': title, 'url': url} for title, url in portals],
           'items': []}
    schools.append(out)
    return out

def item(s, title, year, kind, tags, summary, url, doi, source_type,
         attribution, note, publication_url=None, publication_date=None,
         source_date=None, extra_sources=None):
    s['items'].append({
        'title': title, 'year': year, 'type': kind,
        'topics': [TOPICS[t] for t in tags], 'topic_codes': tags,
        'summary_vi': summary, 'url': url, 'doi': doi,
        'publication_url': publication_url or ('https://doi.org/' + doi if doi else None),
        'publication_date': publication_date, 'source_date': source_date,
        'source_type': source_type, 'university_attribution': attribution,
        'verification_note': note,
        'source_urls': [url] + (extra_sources or []),
        'checked_on': '2026-10-30', 'full_text_read': False,
        'classification_method': 'Phân loại thủ công theo nội dung tóm tắt đã đọc; một công trình có thể thuộc nhiều nhóm.'
    })

s = school('Massachusetts Institute of Technology', 'mit.edu', [
    ('MIT News — nghiên cứu', 'https://news.mit.edu/'),
    ('Danh mục công bố của nhóm Vinod Vaikuntanathan, CSAIL', 'https://people.csail.mit.edu/vinodv/pubs.html')])
item(s, 'Generative-AI-Driven Jumping Robot Design Using Diffusion Models', 2025,
     'conference_paper', ['ai_data', 'robotics'],
     'Dùng mô hình khuếch tán và mô phỏng vật lý để tối ưu hình học robot nhảy có thể in 3D. Thử nghiệm so sánh cho thấy thiết kế mới nhảy cao hơn và tiếp đất ổn định hơn thiết kế cơ sở.',
     'https://news.mit.edu/2025/using-generative-ai-help-robots-jump-higher-land-safely-0627',
     '10.1109/ICRA55743.2025.11128113', 'university_research_news_and_publisher_abstract',
     'MIT CSAIL xác nhận nghiên cứu của Byungchul Kim, Tsun-Hsuan Wang và Daniela Rus.',
     'Đã đọc bản tin MIT và abstract IEEE; bản tin liên kết bản PDF tác giả. Công trình tại ICRA 2025; chưa đánh giá toàn văn hoặc khả năng tái lập.',
     source_date='2025-06-27', extra_sources=['https://doi.org/10.1109/ICRA55743.2025.11128113'])
item(s, 'Somewhat Homomorphic Encryption from Linear Homomorphism and Sparse LPN', 2025,
     'conference_paper', ['security', 'ai_data'],
     'Đề xuất cơ chế mã hóa cho phép thực hiện một số phép tính giới hạn trực tiếp trên dữ liệu mã hóa. Hướng nghiên cứu phục vụ tra cứu cơ sở dữ liệu và phân tích thống kê bảo mật; kết quả đang ở mức xây dựng lý thuyết.',
     'https://news.mit.edu/2025/security-scheme-could-protect-sensitive-data-during-cloud-computation-0319',
     '10.1007/978-3-031-91124-8_1', 'university_research_news_and_publication_list',
     'Bản tin MIT nêu các tác giả thuộc EECS/CSAIL; danh mục của Vinod Vaikuntanathan xác nhận EUROCRYPT 2025.',
     'Đã đọc bản tin trường và thông tin công bố; phân biệt preprint IACR 2024/1760 với bài hội nghị năm 2025. Chưa đọc toàn văn.',
     source_date='2025-03-19', extra_sources=['https://people.csail.mit.edu/vinodv/pubs.html', 'https://link.springer.com/chapter/10.1007/978-3-031-91124-8_1'])

s = school('California Institute of Technology', 'caltech.edu', [
    ('Caltech — tin nghiên cứu chính thức', 'https://www.caltech.edu/about/news'),
    ('Caltech Research', 'https://www.caltech.edu/research')])
item(s, 'Tensor Learning and Compression of N-Phonon Interactions', 2025,
     'journal_article', ['ai_data', 'materials', 'basic_science'],
     'Học và nén tensor biểu diễn tương tác phonon để giảm chi phí tính toán tính chất nhiệt của vật liệu. Phương pháp giữ độ chính xác cao khi tính tốc độ tán xạ phonon và độ dẫn nhiệt trên các vật liệu được khảo sát.',
     'https://www.caltech.edu/about/news/new-ai-technique-unravels-quantum-atomic-vibrations-in-materials',
     '10.1103/nmgj-yq1g', 'university_research_news_and_publisher_abstract',
     'Bản tin Caltech và trang Physical Review Letters ghi nhóm Marco Bernardi, Yao Luo cùng các tác giả thuộc Caltech.',
     'Đã đọc bản tin và abstract nhà xuất bản; chưa đọc phần toàn văn có yêu cầu quyền truy cập.',
     publication_date='2025-09-16', source_date='2025-09-16', extra_sources=['https://journals.aps.org/prl/abstract/10.1103/nmgj-yq1g'])
item(s, 'Supervised learning in DNA neural networks', 2025,
     'journal_article', ['ai_data', 'biotech'],
     'Xây dựng mạng nơ-ron bằng phân tử DNA có thể học từ ví dụ hóa học và nhận dạng mẫu mới. Thông tin học được lưu qua nồng độ và tương tác của các chuỗi DNA, mở hướng nghiên cứu tính toán phân tử và vật liệu thích nghi.',
     'https://www.caltech.edu/about/news/dna-based-neural-network-learns-from-examples-to-solve-problems',
     '10.1038/s41586-025-09479-w', 'university_research_news',
     'Caltech xác nhận nghiên cứu tại phòng thí nghiệm Lulu Qian, với Kevin Cherry là tác giả thứ nhất.',
     'Đã đọc bản tóm lược chính thức của trường và xác nhận trang Nature được liên kết; chưa đọc toàn văn. Các ứng dụng thuốc hoặc vật liệu thông minh là định hướng tương lai.',
     publication_date='2025-09-03', source_date='2025-09-03', extra_sources=['https://www.nature.com/articles/s41586-025-09479-w'])

s = school('Georgia Institute of Technology', 'gatech.edu', [
    ('Georgia Tech — tin nghiên cứu', 'https://news.gatech.edu/'),
    ('EPIC Lab — công bố và dự án', 'https://www.epic.gatech.edu/')])
item(s, 'SAIL: Faster-than-Demonstration Execution of Imitation Learning Policies', 2025,
     'conference_paper', ['ai_data', 'robotics'],
     'Điều chỉnh tốc độ thực thi của robot học từ thao tác mẫu của con người. Hệ thống phối hợp làm mượt chuyển động, bám quỹ đạo và bù độ trễ để tăng tốc nhiều tác vụ thao tác mà vẫn duy trì độ chính xác trong thử nghiệm.',
     'https://www.gatech.edu/news/2026/03/19/smarter-faster-and-more-human-leap-toward-general-purpose-robots',
     '10.48550/arXiv.2506.11948', 'university_research_news',
     'Georgia Tech nêu nhóm Shreyas Kousik, Benjamin Joffe và Danfei Xu, cùng trích dẫn công trình CoRL 2025.',
     'Đã đọc bản tin trường; năm 2025 là năm hội nghị, còn bản tin đăng năm 2026. DOI được trường cung cấp là DOI bản arXiv, không phải DOI riêng của kỷ yếu; chưa đọc toàn văn.',
     publication_url='https://arxiv.org/abs/2506.11948', source_date='2026-03-19')
item(s, 'Deep domain adaptation eliminates costly data required for task-agnostic wearable robotic control', 2025,
     'journal_article', ['ai_data', 'robotics', 'biotech'],
     'Chuyển dữ liệu cơ sinh học sẵn có sang điều khiển bộ khung trợ lực mới bằng thích nghi miền sâu. Mục tiêu là ước lượng mô-men khớp thời gian thực và giảm nhu cầu thu thập dữ liệu riêng cho từng thiết bị, người dùng và tác vụ.',
     'https://www.epic.gatech.edu/keaton-and-carlos-published-a-new-paper-in-science-roboitcs/',
     '10.1126/scirobotics.ads8652', 'official_lab_publication_news',
     'EPIC Lab tại Georgia Tech xác nhận công bố Science Robotics của Keaton Scherpereel và Carlos Carrasquillo.',
     'Đã đọc bản tin phòng thí nghiệm; DOI lấy từ liên kết bài Science Robotics. Trang nhà xuất bản trả 403; chưa đọc abstract nhà xuất bản hoặc toàn văn.',
     source_date='2025-11-30')

s = school('Carnegie Mellon University', 'cmu.edu', [
    ('Software Engineering Institute — thư viện công bố', 'https://www.sei.cmu.edu/library/')])
item(s, 'Sabermetrics for Cyber: Collecting and Analyzing User Activity Data from Ephemeral Exercises', 2025,
     'conference_paper', ['security', 'ai_data'],
     'Đề xuất thu giữ và lưu dữ liệu hành vi người tham gia trong môi trường diễn tập an ninh mạng tạm thời. Dữ liệu giúp phân tích kỹ năng, đánh giá hiệu quả và cải thiện thiết kế hoạt động đào tạo an ninh mạng.',
     'https://www.sei.cmu.edu/library/sabermetrics-for-cyber-collecting-and-analyzing-user-activity-data-from-ephemeral-exercises/',
     '10.34190/eccws.24.1.3354', 'institutional_publication_abstract',
     'Trang công bố của Software Engineering Institute, Carnegie Mellon University, nêu nghiên cứu và tác giả của SEI.',
     'Đã đọc metadata và abstract của SEI; bài hội nghị ECCWS 2025. Chưa đọc toàn văn.',
     publication_date='2025-06-25')
item(s, 'What Can Generative AI Red-Teaming Learn from Cyber Red-Teaming?', 2025,
     'technical_report', ['ai_data', 'security'],
     'Tổng hợp có hệ thống hai dòng nghiên cứu về red teaming: an ninh mạng và AI tạo sinh. Báo cáo xem xét cách chuyển phương pháp đánh giá đối kháng đã có sang kiểm tra độ an toàn của hệ thống AI.',
     'https://sei.cmu.edu/library/what-can-generative-ai-red-teaming-learn-from-cyber-red-teaming/',
     '10.1184/R1/29410136', 'institutional_publication_abstract',
     'Metadata chính thức ghi cơ quan xuất bản Software Engineering Institute, Carnegie Mellon University.',
     'Đã đọc metadata và abstract. Đây là báo cáo kỹ thuật CMU/SEI-2025-TR-006, không gán là bài tạp chí; chưa đọc toàn văn PDF.',
     publication_date='2025-07-16')

s = school('Purdue University', 'purdue.edu', [
    ('Energy and Transport Sciences Laboratory — Publications', 'https://engineering.purdue.edu/ETSL/publication.html'),
    ('Marconnet Thermal and Energy Conversion Lab', 'https://engineering.purdue.edu/MTEC/')])
item(s, 'Electrospun Boron Nitride Nanotube Fabrics: Tunable Thermal Conductivity through Controlled Nanotube Orientation', 2025,
     'journal_article', ['materials', 'energy'],
     'Dùng kéo sợi điện và nhiệt phân để tạo vải ống nano nitride bo có định hướng điều khiển được. Công trình phân tích ảnh hưởng của định hướng, liên kết giữa sợi và chiều dài ống nano lên truyền nhiệt, phục vụ vật liệu quản lý nhiệt.',
     'https://engineering.purdue.edu/MTEC/publications/electrospun-boron-nitride-nanotube-fabrics-tunable-thermal-conductivity-through-controlled-nanotube-orientation',
     '10.1002/adem.202500703', 'official_lab_publication_abstract',
     'Trang công bố của Marconnet Thermal and Energy Conversion Lab thuộc Purdue nêu tác giả A. Marconnet và cộng sự.',
     'Đã đọc metadata và abstract trên trang phòng thí nghiệm. Trang lab ghi Event Date 03/08/2025; không dùng trường này làm ngày xuất bản vì khác metadata Crossref. Chưa đọc toàn văn nhà xuất bản.',
     source_date='2025-08-03')
item(s, 'Consequential Climate and Energy Analysis of Steel Electrification via Hydrogen Direct Reduction', 2025,
     'journal_article', ['energy', 'environment'],
     'Mô hình hóa nhu cầu điện và phát thải khi chuyển sản xuất thép sang khử trực tiếp bằng hydro và lò hồ quang điện. Kết quả nhấn mạnh việc phối hợp nhà máy điện phân với cơ cấu nguồn điện, đặc biệt điện gió và mặt trời.',
     'https://engineering.purdue.edu/ETSL/publication.html',
     '10.1021/acsenergylett.5c01961', 'official_lab_publication_abstract_and_publisher_abstract',
     'Danh mục ETSL và metadata ACS ghi các tác giả thuộc các trường kỹ thuật của Purdue.',
     'Đã đọc abstract ở danh mục phòng thí nghiệm và ACS. Các kết quả phát thải là dự báo theo kịch bản, không phải mức giảm đã xảy ra; chưa đọc toàn văn.',
     publication_date='2025-09-02', extra_sources=['https://pubs.acs.org/doi/10.1021/acsenergylett.5c01961'])

s = school('Rensselaer Polytechnic Institute', 'rpi.edu', [
    ('RPI — tin nghiên cứu chính thức', 'https://news.rpi.edu/')])
item(s, 'Atomic lift-off of epitaxial membranes for cooling-free infrared detection', 2025,
     'journal_article', ['materials', 'electronics_telecom'],
     'Phát triển phương pháp tách màng tinh thể siêu mỏng mà không cần lớp giải phóng nhân tạo. Màng vật liệu nhiệt điện được nghiên cứu cho cảm biến hồng ngoại không cần làm lạnh; nhóm RPI đóng góp tính toán cơ chế liên kết tại bề mặt tiếp xúc.',
     'https://news.rpi.edu/2025/08/18/nanomanufacturing-breakthrough-could-revolutionize-night-vision-technology-other-fields',
     '10.1038/s41586-025-08874-7', 'university_research_news',
     'RPI xác nhận Yunfeng Shi là đồng tác giả lãnh đạo phần tính toán; đây là hợp tác với MIT và các trường khác.',
     'Đã đọc bản tin RPI và đối chiếu tên bài, DOI, ngày công bố Nature. Bản tin tháng 8 khác ngày xuất bản bài báo tháng 4; chưa đọc toàn văn.',
     publication_date='2025-04-23', source_date='2025-08-18', extra_sources=['https://www.nature.com/articles/s41586-025-08874-7'])
item(s, 'Dimensionality and dynamics for next-generation artificial neural networks', 2025,
     'journal_article', ['ai_data'],
     'Thảo luận thiết kế mạng nơ-ron tăng cấu trúc theo chiều không gian và bổ sung vòng phản hồi theo thời gian. Định hướng lấy cảm hứng từ não bộ nhằm cải thiện biểu diễn, khả năng học và hiệu quả sử dụng tài nguyên của AI.',
     'https://news.rpi.edu/2025/06/16/ai-rethought-rpi-researchers-propose-more-effective-human-approach',
     '10.1016/j.patter.2025.101231', 'university_research_news',
     'RPI ghi nghiên cứu do Ge Wang của RPI và Fenglei Fan của City University of Hong Kong dẫn dắt.',
     'Đã đọc bản tin trường; dùng tên bài đầy đủ từ trang nhà xuất bản Patterns, bổ sung từ artificial mà bản tin rút gọn. Nội dung là định hướng kiến trúc, không suy diễn đã triển khai thương mại; chưa đọc toàn văn.',
     source_date='2025-06-12', extra_sources=['https://doi.org/10.1016/j.patter.2025.101231'])

s = school('Virginia Polytechnic Institute and State University', 'vt.edu', [
    ('VTechWorks — kho nghiên cứu Virginia Tech', 'https://vtechworks.lib.vt.edu/'),
    ('Virginia Tech News', 'https://news.vt.edu/')])
item(s, 'Combining and Decoupling Rigid and Soft Grippers to Enhance Robotic Manipulation', 2025,
     'journal_article', ['robotics', 'materials'],
     'Kết hợp kẹp cứng với bề mặt bám dính mềm có thể bật/tắt để robot thao tác nhiều loại vật thể. Thiết kế và điều khiển hỗ trợ người dùng thực hiện các tác vụ hằng ngày, được minh họa bằng việc chuẩn bị đồ ăn.',
     'https://news.vt.edu/articles/2025/07/eng-me-losey-bartlett-pizza-robot.html',
     '10.1089/soro.2024.0062', 'university_research_news_and_publisher_abstract',
     'Bản tin Virginia Tech xác nhận nhóm Dylan Losey và Michael Bartlett; trang bài báo liệt kê nhóm tác giả tương ứng.',
     'Đã đọc bản tin trường và abstract Soft Robotics. DOI chứa 2024 nhưng bài được xuất bản trực tuyến năm 2025; chưa đọc toàn văn.',
     publication_date='2025-03-10', source_date='2025-07-28', extra_sources=['https://journals.sagepub.com/doi/abs/10.1089/soro.2024.0062'])
item(s, 'Game-Theoretic and Machine Learning-based Defensive Deception for Dependable and Secure Cyber-Physical Systems', 2025,
     'doctoral_dissertation', ['security', 'ai_data', 'robotics'],
     'Kết hợp lý thuyết trò chơi và học máy để xây dựng phòng thủ đánh lừa đối phương trong hệ thống vật lý số và nhóm người–máy. Luận án khảo sát IoT, nhiệm vụ UAV và phối hợp người với robot mặt đất trước các mối đe dọa mạng.',
     'https://vtechworks.lib.vt.edu/items/c5ae72d9-407f-420b-940b-878c7ca919ff',
     None, 'institutional_repository_abstract',
     'VTechWorks ghi tác giả Zelin Wan, đơn vị xuất bản Virginia Tech và bộ sưu tập Doctoral Dissertations.',
     'Đã đọc metadata và abstract trong kho trường; đây là luận án tiến sĩ, chưa đọc toàn văn PDF. Kho cung cấp Handle, không thấy DOI trong metadata đã đọc.',
     publication_url='https://hdl.handle.net/10919/135538', publication_date='2025-06-18')

s = school('Texas A&M University', 'tamu.edu', [
    ('Texas A&M Engineering News', 'https://news.engineering.tamu.edu/'),
    ('Texas A&M Stories', 'https://stories.tamu.edu/')])
item(s, 'Organic dual-ion batteries with low-temperature operability and structural reinforcement', 2025,
     'journal_article', ['energy', 'materials'],
     'Kết hợp điện cực polymer hoạt tính oxy hóa-khử với chất điện phân chịu lạnh để pin vẫn hoạt động dưới nhiệt độ âm sâu. Sợi carbon đồng thời làm bộ thu dòng và gia cường cơ học, hướng tới pin vừa tích trữ điện vừa chịu lực.',
     'https://stories.tamu.edu/news/2026/02/11/building-batteries-that-dont-break-in-the-cold/',
     '10.1039/D5TA01626F', 'university_research_news',
     'Texas A&M xác nhận nhóm Jodie Lutkenhaus của College of Engineering thực hiện nghiên cứu.',
     'Đã đọc bản tin trường và trích dẫn bài báo. Bài báo thuộc năm 2025; bản tin được đăng tháng 2/2026. Chưa đọc toàn văn.',
     source_date='2026-02-11')
item(s, 'Graphene oxide synthesis at a nonthermal plasma-water interface', 2026,
     'journal_article', ['materials', 'energy', 'environment'],
     'Tổng hợp graphene oxide trực tiếp từ methane tại bề mặt tiếp xúc plasma không nhiệt và nước, đồng thời tạo hydro. Công trình tìm hướng sản xuất vật liệu carbon có giá trị từ nguyên liệu khí, phục vụ nghiên cứu pin, điện tử và chế tạo.',
     'https://news.engineering.tamu.edu/news/2026/07/03/unexpected-discovery-yields-new-graphene-oxide-production-method/',
     '10.1038/s41467-026-69831-0', 'university_research_news_and_publisher_metadata',
     'Texas A&M Engineering xác nhận nghiên cứu của nhóm David Staack, Micah Green và các cộng sự công nghiệp.',
     'Đã đọc bản tin trường và kiểm tra tên bài, DOI, ngày công bố qua metadata nhà xuất bản/Crossmark. Chưa đọc toàn văn; không tự suy ra cân bằng phát thải vòng đời.',
     publication_date='2026-02-19', source_date='2026-07-03', extra_sources=['https://www.nature.com/articles/s41467-026-69831-0', 'https://crossmark.crossref.org/dialog/?doi=10.1038%2Fs41467-026-69831-0'])

s = school('Stevens Institute of Technology', 'stevens.edu', [
    ('Stevens Research Portal', 'https://researchwith.stevens.edu/en/')])
item(s, 'Probing Curved Spacetime with a Distributed Atomic Processor Clock', 2025,
     'journal_article', ['basic_science', 'electronics_telecom'],
     'Đề xuất mạng đồng hồ nguyên tử liên kết lượng tử đặt ở các độ cao khác nhau để kiểm tra tương tác giữa lý thuyết lượng tử và độ cong không-thời gian. Đây là thiết kế thí nghiệm và phân tích lý thuyết sử dụng công nghệ mạng lượng tử.',
     'https://researchwith.stevens.edu/en/publications/probing-curved-spacetime-with-a-distributed-atomic-processor-cloc/',
     '10.1103/q188-b1cr', 'institutional_publication_abstract_and_publisher_abstract',
     'Kho công bố Stevens và PRX Quantum ghi Igor Pikovski thuộc Department of Physics, Stevens Institute of Technology.',
     'Đã đọc metadata/abstract và bản tin Stevens; chưa đọc toàn bộ bài. Phương án mới được đề xuất, không trình bày như thí nghiệm đã hoàn tất.',
     publication_date='2025-07-21', extra_sources=['https://journals.aps.org/prxquantum/abstract/10.1103/q188-b1cr', 'https://www.stevens.edu/news/quantum-internet-meets-space-time-in-this-new-ingenious-idea'])
item(s, 'Temporal Contrastive Learning for Sensor-Based Human Activity Recognition: A Self-Supervised Approach', 2025,
     'journal_article', ['ai_data', 'electronics_telecom'],
     'Học biểu diễn chuỗi thời gian cảm biến bằng quan hệ đồng xuất hiện theo thời gian để giảm nhu cầu dữ liệu có nhãn. Khung TCLHAR kết hợp thông tin nhiều loại cảm biến và được đánh giá trên các tập dữ liệu nhận dạng hoạt động người.',
     'https://researchwith.stevens.edu/en/publications/temporal-contrastive-learning-for-sensor-based-human-activity-rec/',
     '10.1109/JSEN.2024.3491933', 'institutional_publication_abstract',
     'Stevens Research Portal gắn công bố với Hao Wang và Department of Electrical and Computer Engineering; đồng thời ghi đối tác Louisiana State University.',
     'Đã đọc metadata và abstract trong cổng nghiên cứu Stevens. Năm tạp chí là 2025 mặc dù DOI chứa 2024; chưa đọc toàn văn.',
     extra_sources=[])

s = school('Illinois Institute of Technology', 'iit.edu', [
    ('Illinois Tech — nghiên cứu', 'https://www.iit.edu/research'),
    ('Illinois Tech — tin chính thức', 'https://www.iit.edu/news')])
item(s, 'STRIFE: A Socio-Technical Framework for Threat Modeling of Artificial Intelligence Systems', 2025,
     'journal_article', ['ai_data', 'security'],
     'Khung mô hình hóa mối đe dọa AI kết hợp góc nhìn kỹ thuật, đạo đức và pháp lý. Công trình xem xét rủi ro phát sinh trong toàn bộ vòng đời hệ thống và mối liên hệ với bối cảnh con người, tổ chức và xã hội.',
     'https://www.iit.edu/news/researchers-introduce-socio-technical-approach-ai-threat-modeling',
     '10.4018/IJIIT.370967', 'university_research_news_and_publisher_metadata',
     'Illinois Tech xác nhận hai đồng tác giả Anuradha/Ann Rangarajan và Saran Ghatak; metadata của nhà xuất bản ghi affiliation Illinois Institute of Technology.',
     'Đã đọc bản tin trường và thông tin đầu bài/abstract được lập chỉ mục của nhà xuất bản. Chưa đọc toàn văn; bản tin không phải chính bài nghiên cứu.',
     source_date='2025-10-29', extra_sources=['https://www.igi-global.com/viewtitle.aspx?titleid=370967'])
item(s, 'Anion sublattice design enables superionic conductivity in crystalline oxyhalides', 2025,
     'journal_article', ['materials', 'energy'],
     'Thiết kế mạng anion hỗn hợp cho chất điện phân rắn oxyhalide giúp ion lithium di chuyển qua các kênh trong tinh thể. Nghiên cứu vật liệu lithium tantalum oxychloride nhằm cải thiện pin thể rắn, bao gồm khả năng hoạt động ở nhiệt độ thấp.',
     'https://www.iit.edu/news/tracking-hidden-highways-build-better-batteries',
     '10.1126/science.adt9678', 'university_research_news',
     'Illinois Tech mô tả đóng góp xác định vị trí lithium của James Kaduk trong nhóm hợp tác quốc tế; đây không phải công trình chỉ của một trường.',
     'Đã đọc bản tin trường, kiểm tra liên kết DOI và metadata Science. Bài báo xuất bản năm 2025, bản tin trường ngày 05/01/2026; chưa đọc toàn văn.',
     publication_date='2025-10-09', source_date='2026-01-05', extra_sources=['https://www.science.org/doi/10.1126/science.adt9678'])

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import TOPICS as CANONICAL_TOPICS

# Manual interpretation of the works, not classification by university name or
# keywords in press-release application examples. The first code is primary.
canonical_tags = {
    'Generative-AI-Driven Jumping Robot Design Using Diffusion Models': ['ROBOTICS', 'AI_DATA'],
    'Somewhat Homomorphic Encryption from Linear Homomorphism and Sparse LPN': ['CYBERSECURITY', 'COMPUTING'],
    'Tensor Learning and Compression of N-Phonon Interactions': ['MATERIALS', 'AI_DATA', 'BASIC_SCIENCE'],
    'Supervised learning in DNA neural networks': ['BIOTECH_HEALTH', 'AI_DATA', 'COMPUTING'],
    'SAIL: Faster-than-Demonstration Execution of Imitation Learning Policies': ['ROBOTICS', 'AI_DATA'],
    'Deep domain adaptation eliminates costly data required for task-agnostic wearable robotic control': ['ROBOTICS', 'AI_DATA', 'BIOTECH_HEALTH'],
    'Sabermetrics for Cyber: Collecting and Analyzing User Activity Data from Ephemeral Exercises': ['CYBERSECURITY', 'COMPUTING'],
    'What Can Generative AI Red-Teaming Learn from Cyber Red-Teaming?': ['CYBERSECURITY', 'AI_DATA'],
    'Electrospun Boron Nitride Nanotube Fabrics: Tunable Thermal Conductivity through Controlled Nanotube Orientation': ['MATERIALS'],
    'Consequential Climate and Energy Analysis of Steel Electrification via Hydrogen Direct Reduction': ['ENERGY', 'ENVIRONMENT'],
    'Atomic lift-off of epitaxial membranes for cooling-free infrared detection': ['MATERIALS', 'ELECTRONICS_TELECOM'],
    'Dimensionality and dynamics for next-generation artificial neural networks': ['AI_DATA'],
    'Combining and Decoupling Rigid and Soft Grippers to Enhance Robotic Manipulation': ['ROBOTICS', 'MATERIALS'],
    'Game-Theoretic and Machine Learning-based Defensive Deception for Dependable and Secure Cyber-Physical Systems': ['CYBERSECURITY', 'AI_DATA', 'ROBOTICS'],
    'Organic dual-ion batteries with low-temperature operability and structural reinforcement': ['ENERGY', 'MATERIALS'],
    'Graphene oxide synthesis at a nonthermal plasma-water interface': ['MATERIALS', 'ENERGY'],
    'Probing Curved Spacetime with a Distributed Atomic Processor Clock': ['BASIC_SCIENCE', 'ELECTRONICS_TELECOM'],
    'Temporal Contrastive Learning for Sensor-Based Human Activity Recognition: A Self-Supervised Approach': ['AI_DATA', 'ELECTRONICS_TELECOM'],
    'STRIFE: A Socio-Technical Framework for Threat Modeling of Artificial Intelligence Systems': ['CYBERSECURITY', 'AI_DATA'],
    'Anion sublattice design enables superionic conductivity in crystalline oxyhalides': ['ENERGY', 'MATERIALS'],
}
for school_record in schools:
    for record in school_record['items']:
        codes = canonical_tags[record['title']]
        assert all(c in CANONICAL_TOPICS for c in codes)
        record['topic_codes'] = codes
        record['primary_topic_code'] = codes[0]
        record['secondary_topic_codes'] = codes[1:]
        record['topics'] = [CANONICAL_TOPICS[c][0] for c in codes]

out = {
    'checked_on': '2026-10-30',
    'scope': 'Đợt quét có chọn lọc: 10 đại học công nghệ/kỹ thuật tại Hoa Kỳ, mỗi trường 2 công trình; không phải toàn bộ công bố của trường hoặc bảng xếp hạng.',
    'selection_method': 'Tìm trên website chính thức của trường, kho nghiên cứu và trang phòng thí nghiệm; ưu tiên công trình 2023–2026 có nội dung và quan hệ tác giả–trường xác minh được. Đối chiếu trang nhà xuất bản khi cần tên chính xác, DOI hoặc ngày công bố.',
    'reading_depth': 'Metadata, abstract và bản tóm lược chính thức. Không công trình nào được đánh dấu đã đọc toàn văn đầy đủ.',
    'topic_taxonomy': {c: label for c, (label, _) in CANONICAL_TOPICS.items()},
    'schools': schools,
}
path = Path('/home/ubuntu/university_research/parts/us_research.json')
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'path': str(path), 'schools': len(schools), 'items': sum(len(s['items']) for s in schools), 'doi_count': sum(bool(i['doi']) for s in schools for i in s['items'])}, ensure_ascii=False))
