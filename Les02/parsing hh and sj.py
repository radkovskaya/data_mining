from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import time
import pandas as pd
main_hh = ('https://hh.ru')
main_sj = ('https://www.superjob.ru')
page_hh = 3
page_sj = 3
vacancy = 'manager'

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
vacancys_url_hh = main_hh + '/search/vacancy?enable_snippets=true&search_fiel=name&showClusters=true&text=' + vacancy
vacancys_url_sj = main_sj + '/vacancy/search?keywords=' + vacancy

vacancys = []
i = 0
for i in range(0, page_hh):
    html_hh = requests.get(vacancys_url_hh, headers = header).text
    parsed_html_hh = bs(html_hh,'lxml')

    vacancy_block = parsed_html_hh.find('div',{'class':'vacancy-serp'})
    vacancy_list = vacancy_block.findChildren(recursive=False)

    for vacancy in vacancy_list:
        vacancy_data = {}
        main_info = vacancy.find('a',{'class':'bloko-link HH-LinkModifier'})
        salary = vacancy.find('div',{'class':'vacancy-serp-item__compensation'})
        if not main_info:
            continue
        else:
            vacancy_name = main_info.getText()
            vacancy_link = main_info['href']
            if not salary:
                min_salary = 'not_defined'
                max_salary = 'not_defined'
            else:
                vacancy_salary = salary.getText().replace('\xa0', '').replace('.','')
                if "от" in vacancy_salary:
                    min_salary = vacancy_salary[3:]
                    max_salary = 'not_defined'
                elif "до" in vacancy_salary:
                    min_salary = 'not_defined'
                    max_salary = vacancy_salary[3:]
                elif "-" in vacancy_salary:
                    tmp_sal = vacancy_salary.split("-")
                    min_salary = tmp_sal[0] + " "+ tmp_sal[1][-3:]
                    max_salary = tmp_sal[1]
                else:
                    min_salary = 'error'
                    max_salary = 'error'
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['min_salary '] = min_salary
            vacancy_data['max_salary '] = max_salary
            vacancy_data['cite'] = main_hh
            vacancys.append(vacancy_data)
    next_page = parsed_html_hh.find('a', {'class': 'HH-Pager-Controls-Next'})['href']
    vacancys_url_hh = main_hh + next_page
    time.sleep(1)
    i += 1

j = 0
for j in range(0, page_sj):
    html_sj = requests.get(vacancys_url_sj, headers=header).text
    parsed_html_sj = bs(html_sj, 'lxml')

    vacancy_block_sj = parsed_html_sj.find('div',{'style':'display:block'})
    vacancy_list_sj = vacancy_block_sj.findChildren(recursive=False)

    for vacancy in vacancy_list_sj:
            vacancy_data = {}
            main_info = vacancy.find('a', {'class': "_1QIBo"})
            if not main_info:
                continue
            else:
                vacancy_name = main_info.getText()
                vacancy_link = main_sj + main_info['href']
                salary = vacancy.find('span', {'class': '_2Wp8I'})
                vacancy_salary = salary.getText().replace('\xa0', '').replace('.', '')
                if vacancy_salary.startswith("от"):
                    min_salary = vacancy_salary[2:-1] + " " + vacancy_salary[-1:]
                    max_salary = 'not_defined'
                elif vacancy_salary.startswith("до"):
                    min_salary = 'not_defined'
                    max_salary = vacancy_salary[3:]
                elif "—" in vacancy_salary:
                    tmp_sal = vacancy_salary.split("—")
                    min_salary = tmp_sal[0] + " " + tmp_sal[1][-1:]
                    max_salary = tmp_sal[1][:-1] + ' ' + tmp_sal[1][-1:]
                else:
                    min_salary = 'not_defined'
                    max_salary = 'not_defined'
                vacancy_data['name'] = vacancy_name
                vacancy_data['link'] = vacancy_link
                vacancy_data['min_salary '] = min_salary
                vacancy_data['max_salary '] = max_salary
                vacancy_data['cite'] = main_sj
                vacancys.append(vacancy_data)
    next_page = parsed_html_sj.find('a', {'class': 'f-test-button-dalshe'})['href']

    vacancys_url_sj = main_sj + next_page
    time.sleep(1)
    j += 1

pprint(vacancys)
print(len(vacancys))

df = pd.DataFrame(vacancys)
print(df)