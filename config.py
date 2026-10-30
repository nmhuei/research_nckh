from pathlib import Path
import re, unicodedata

ROOT = Path(__file__).resolve().parent
DATE = '2026-10-30'
# Europe + countries participating in the wider European higher-education area.
EUROPE = set('AL AD AM AT AZ BA BE BG BY CH CY CZ DE DK EE ES FI FR GB GE GR HR HU IE IS IT KZ LI LT LU LV MC MD ME MK MT NL NO PL PT RO RS RU SE SI SK SM TR UA VA XK FO GI GG IM JE'.split())
SEEDS = [
 ('USTH','VN','usth.edu.vn'),('HUST','VN','hust.edu.vn'),('UET','VN','uet.vnu.edu.vn'),
 ('HCMUT','VN','hcmut.edu.vn'),('UIT','VN','uit.edu.vn'),('PTIT','VN','ptit.edu.vn'),
 ('DUT','VN','dut.udn.vn'),('VKU','VN','vku.udn.vn'),('HCMUTE','VN','hcmute.edu.vn'),
 ('VLUTE','VN','vlute.edu.vn'),('MTA','VN','mta.edu.vn'),('KMA','VN','actvn.edu.vn'),
 ('UTC','VN','utc.edu.vn'),('HUMG','VN','humg.edu.vn'),('HUCE','VN','huce.edu.vn'),
 ('FPT','VN','fpt.edu.vn'),('Phenikaa','VN','phenikaa-uni.edu.vn'),
 ('MIT','US','mit.edu'),('Caltech','US','caltech.edu'),('Georgia Tech','US','gatech.edu'),
 ('CMU','US','cmu.edu'),('Purdue','US','purdue.edu'),('RPI','US','rpi.edu'),
 ('Virginia Tech','US','vt.edu'),('Texas A&M','US','tamu.edu'),('Stevens','US','stevens.edu'),('IIT','US','iit.edu'),
 ('ETH Zurich','CH','ethz.ch'),('EPFL','CH','epfl.ch'),('Imperial','GB','imperial.ac.uk'),
 ('TU Delft','NL','tudelft.nl'),('TU/e','NL','tue.nl'),('RWTH Aachen','DE','rwth-aachen.de'),
 ('TUM','DE','tum.de'),('TU Berlin','DE','tu.berlin'),('KTH','SE','kth.se'),
 ('Chalmers','SE','chalmers.se'),('Aalto','FI','aalto.fi'),('Politecnico di Milano','IT','polimi.it'),
 ('Politecnico di Torino','IT','polito.it'),('TU Wien','AT','tuwien.at')]
ALIASES = {'tu-berlin.de':'tu.berlin','tuwien.ac.at':'tuwien.at','uet.edu.vn':'uet.vnu.edu.vn','phenikaa.edu.vn':'phenikaa-uni.edu.vn'}

TOPICS = {
 'AI_DATA': ('AI, học máy và dữ liệu',r'\b(artificial intelligence|machine learning|deep learning|neural|llm|large language|generative|reinforcement|federated|data mining|data science|computer vision|recognition|yolo|bert|transformer|prediction|forecast|tri tue nhan tao|hoc may|hoc sau|du lieu|nhan dang|nhan dien)\b'),
 'CYBERSECURITY': ('An ninh mạng và mật mã',r'cyber|security|cryptograph|malware|intrusion|privacy|encryption|encrypted|vulnerability|phishing|bao mat|an toan thong tin|mat ma|an ninh mang'),
 'COMPUTING': ('Phần mềm, hệ thống tính toán và mạng',r'\b(software|computing|computer|cloud|hpc|distributed|database|code|sql|algorithms?|optimization|optimisation|phan mem|tinh toan|co so du lieu|he thong thong tin)\b'),
 'ELECTRONICS_TELECOM': ('Điện tử, bán dẫn, viễn thông và IoT',r'\b(semiconductor|chip|circuit|photon|wireless|mimo|5g|6g|telecom|iot|lora|lorawan|sensor|electronics|quantum|ban dan|vi mach|cam bien|vien thong|dien tu)\b'),
 'ROBOTICS': ('Robot, điều khiển và tự động hóa',r'robot|autonomous|automation|control|uav|drone|mechatron|tu dong|dieu khien|co dien tu'),
 'MATERIALS': ('Vật liệu, nano và công nghệ hóa học',r'material|nano|polymer|alloy|cataly|membrane|chemical|vat lieu|hop kim|xuc tac|hoa hoc'),
 'ENERGY': ('Năng lượng và công nghệ điện',r'\b(energy|battery|batteries|solar|hydrogen|photovoltaic|wind|power grid|nuclear fusion|nuclear energy|nang luong|dien mat troi|pin|dien gio)\b'),
 'ENVIRONMENT': ('Môi trường, khí hậu và tài nguyên',r'environ|climate|pollut|carbon capture|carbon emission|emission|flood|water|waste|hydrolog|geolog|earth|aquifer|biochar|\bmining\b|moi truong|khi hau|phat thai|nuoc|lu lut|dia chat'),
 'BIOTECH_HEALTH': ('Công nghệ sinh học và kỹ thuật y sinh',r'biotech|biomed|medical|health|diagnos|drug|disease|protein|genom|bacteria|cancer|tissue|blood cell|stem cell|cell culture|sinh hoc|y sinh|benh|suc khoe'),
 'CONSTRUCTION_TRANSPORT': ('Xây dựng, giao thông và cơ khí',r'\b(traffic|transport|vehicle|mobility|civil engineering|construction|structural|concrete|bridge|mechanical|fluid|aerodynamic|giao thong|xay dung|be tong|co khi|o to|phuong tien)\b'),
 'AGRI_FOOD': ('Công nghệ nông nghiệp và thực phẩm',r'agricultur|farm|crop|food|greenhouse|nong nghiep|thuc pham|cay trong'),
 'BASIC_SCIENCE': ('Khoa học nền tảng phục vụ công nghệ',r'\b(mathematic|physics|theorem|topolog|astronom|cosmolog|vat ly|toan hoc)\b'),
 'OTHER': ('Khác hoặc chưa đủ dữ liệu phân loại',r'(?!)'),
}
def plain(s):
 return ''.join(c for c in unicodedata.normalize('NFD',s.lower().replace('đ','d')) if unicodedata.category(c)!='Mn')
def classify(s):
 text=plain(s)
 out=[k for k,(_,pat) in TOPICS.items() if re.search(pat,text,re.I)]
 return out or ['OTHER']
TECH_PATTERN = re.compile(r'technolog|technisch|technic|teknik|tecnolog|tecnico|polytech|politec|politech|engineering|ingenieur|ingegner|ingenier|applied sciences|cong nghe|ky thuat|bach khoa|vien thong|mo - dia chat|xay dung|giao thong|dien luc|cong nghiep',re.I)
