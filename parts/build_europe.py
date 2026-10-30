import csv,json,re,collections
from pathlib import Path
from urllib.parse import urlsplit
BASE=Path('/home/ubuntu/university_research'); RAW=BASE/'raw/europe'; OUT=BASE/'parts'
countrycodes={'Albania':'AL','Andorra':'AD','Armenia':'AM','Austria':'AT','Azerbaijan':'AZ','Belarus':'BY','Belgium':'BE','Bosnia and Herzegovina':'BA','Bulgaria':'BG','Croatia':'HR','Cyprus':'CY','Czech Republic':'CZ','Denmark':'DK','Estonia':'EE','Finland':'FI','France':'FR','Georgia':'GE','Germany':'DE','Greece':'GR','Holy See':'VA','Hungary':'HU','Iceland':'IS','Ireland':'IE','Italy':'IT','Kazakhstan':'KZ','Kosovo':'XK','Latvia':'LV','Liechtenstein':'LI','Lithuania':'LT','Luxembourg':'LU','Malta':'MT','Moldova':'MD','Monaco':'MC','Montenegro':'ME','Netherlands':'NL','North Macedonia':'MK','Norway':'NO','Poland':'PL','Portugal':'PT','Romania':'RO','Russia':'RU','San Marino':'SM','Serbia':'RS','Slovakia':'SK','Slovenia':'SI','Spain':'ES','Sweden':'SE','Switzerland':'CH','Türkiye':'TR','Ukraine':'UA','United Kingdom':'GB'}
raw=list(csv.DictReader((RAW/'deqar-institutions.csv').open(encoding='utf-8-sig')))
counts=collections.Counter(); rows=[];seen=set()
def web(x):
 x=(x or '').strip()
 if not x or x.lower() in ['n/a','none','null','-']:return None
 if not re.match('https?://',x):x='https://'+x
 try:
  d=urlsplit(x).hostname
  if not d or '.' not in d or ' ' in d:return None
 except:return None
 return x
def domain(x):return urlsplit(x).hostname.lower().removeprefix('www.')
for x in raw:
 country=x['country'].split(' (')[0]
 if country not in countrycodes:counts['outside_scope_or_missing_country']+=1;continue
 if x['closure_date'] and x['closure_date']<='2026-10-30':counts['closed']+=1;continue
 u=web(x['website_link'])
 if not u:counts['missing_or_invalid_website']+=1;continue
 # Constituent faculties/campuses generally have no ETER ID and a named parent. Preserve separately.
 if not x['eter_id'] and x['parent_institution']:counts['constituent_no_eter_with_parent']+=1;continue
 if x['deqar_id'] in seen:counts['duplicate_deqar_id']+=1;continue
 seen.add(x['deqar_id'])
 note='Website listed in EQAR/DEQAR nightly institution export (2026-10-30); individual website not live-tested. Absence of a closure date is not independent proof of current accreditation.'
 r={'name':x['name_primary'],'country':country,'country_code':countrycodes[country],'website':u,'domains':[domain(u)],'source_urls':[x['deqar_url'],'https://www.eqar.eu/qa-results/download-data-sets/'],'source_tier':'european_registry','institution_type':'higher education institution (registry classification)','verification_note':note,'name_official':x['name_official'],'eter_id':x['eter_id'],'deqar_id':x['deqar_id'],'registry_identifiers':x['identifiers_all'],'parent_institution':x['parent_institution']}
 if x['parent_institution']:r['verification_note']+=' Registry records a parent or alliance relationship: '+x['parent_institution']+'.'
 if country=='Kosovo':r['verification_note']+=' XK is a user-assigned code, not an ISO 3166-1 assignment.'
 rows.append(r)
# authoritative current URLs for domains explicitly encountered during checking
for r in rows:
 if r['eter_id']=='DE0029':
  r['website']='https://www.tu.berlin/en/';r['domains']=['tu.berlin','tu-berlin.de'];r['source_urls'].append(r['website']);r['verification_note']+=' Current public university site confirms tu.berlin; source retained the legacy tu-berlin.de domain.'
 if r['eter_id']=='AT0005':
  r['website']='https://www.tuwien.at/en/';r['domains']=['tuwien.at','tuwien.ac.at'];r['source_urls'].append(r['website']);r['verification_note']+=' Current official university home page confirms tuwien.at; source retained legacy tuwien.ac.at.'
fr=json.loads((RAW/'fr-esr-principaux.json').read_text());added=0;matched=0
frbase='https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-principaux-etablissements-enseignement-superieur/'
for f in fr:
 u=web(f['url'])
 if not u:continue
 source=frbase+'?refine.etablissement_id_paysage='+f['etablissement_id_paysage']
 matches=[r for r in rows if r['country_code']=='FR' and ((f.get('identifiant_eter') and r.get('eter_id')==f['identifiant_eter']) or (domain(u) in r['domains'] and (r['name_official']==f['uo_lib'] or r['name']==f.get('uo_lib_en'))))]
 if matches:
  r=matches[0];r['source_urls'].append(source);r['source_tier']='government_registry';r['website']=u;r['domains']=sorted(set(r['domains']+[domain(u)]));r['institution_type']='; '.join(f.get('type_d_etablissement') or ['higher education institution']);r['verification_note']+=' Corroborated by French ministry principal-institutions dataset, retrieved 2026-10-30 (metadata modified 2025-02-26; data processed 2026-10-30). Ministry URL takes priority.';matched+=1
 else:
  rows.append({'name':f['uo_lib'],'country':'France','country_code':'FR','website':u,'domains':[domain(u)],'source_urls':[source],'source_tier':'government_registry','institution_type':'; '.join(f.get('type_d_etablissement') or ['higher education institution']),'verification_note':'Listed in French ministry principal-institutions dataset retrieved 2026-10-30. Metadata modified 2025-02-26; data processed 2026-10-30. The dataset includes overseas French establishments and excludes components of experimental public institutions.','eter_id':f.get('identifiant_eter'),'ror_ids':f.get('identifiant_ror') or []});added+=1
rows.sort(key=lambda r:(r['country'],r['name']))
(OUT/'europe_official.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
notes={'retrieved_on':'2026-10-30','sources':[{'name':'EQAR Database of External Quality Assurance Results (DEQAR), HEI export','landing_url':'https://www.eqar.eu/qa-results/download-data-sets/','download_url':'https://backend.deqar.eu/static/daily-csv/deqar-institutions.csv','last_modified_http':'2026-10-30T13:00:27Z','license':'Open Data Commons PDDL','coverage':'Source intends comprehensive tertiary-institution coverage of EHEA, based on ETER/OrgReg plus agency input; source also contains non-European records. This file selects European/EHEA countries including Türkiye, Armenia, Azerbaijan, Georgia, Kazakhstan; excludes unspecified country and closed institutions.','raw_rows':len(raw),'filters_excluded':dict(counts),'limitations':['DEQAR inclusion is not itself proof of recognised degree-awarding powers or active accreditation.','URLs inherited from a registry can be stale; no bulk live HTTP/DNS check performed.','Faculties/campuses with no ETER ID and a parent institution excluded to reduce department duplication. This heuristic can exclude some affiliated providers.','Missing-country records excluded rather than guessing location from ETER ID.','XK for Kosovo is user-assigned and not formally ISO2.']},{'name':'French Ministry: Principaux établissements d’enseignement supérieur','landing_url':frbase,'download_url':'https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-principaux-etablissements-enseignement-superieur/exports/json','raw_rows':len(fr),'corroborated_rows':matched,'additional_rows':added,'metadata_modified':'2025-02-26T13:10:40Z','data_processed':'2026-10-30T04:01:57Z','license':'Licence Ouverte v2.0 (Etalab)','limitations':['Main institutions only, not all French higher education providers.','Excludes constituent establishments of experimental or formerly experimental public institutions.','French scope includes overseas territories; country here records national education-system affiliation, not a strict geographic classification.']}],'not_ingested':[{'name':'HRK Hochschulkompass','url':'https://www.hochschulkompass.de/en/higher-education-institutions/downloads.html','reason':'Public bulk download exists; page limits free use to personal use and requires permission for other reuse. Retained as verification route rather than importing bulk rows.'},{'name':'European Higher Education Sector Observatory / former ETER','url':'https://national-policies.eacea.ec.europa.eu/eheso','reason':'Former eter-project.com redirects to EHESO. Public benchmarking pages found; DEQAR supplies accessible ETER/OrgReg-derived institution dump, so a separate EHESO institution export was not ingested.'}],'national_verification_index':json.loads((RAW/'enic-links.json').read_text()),'national_index_note':'ENIC-NARIC official country pages list national recognised-institution directories; links extracted from their Recognised Higher Education Institutions section. All EU27, UK, Switzerland, Norway, Iceland and Liechtenstein covered. These are verification routes, not evidence that each compiled institution was individually checked.','total_rows':len(rows),'country_counts':dict(sorted(collections.Counter(r['country'] for r in rows).items()))}
(OUT/'europe_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print(json.dumps({'total_rows':len(rows),'countries':len(notes['country_counts']),'excluded':dict(counts),'fr_matched':matched,'fr_added':added},indent=2))
