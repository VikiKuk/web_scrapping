from pprint import pprint
import fake_headers
import requests
from bs4 import BeautifulSoup
import json


def gen_headers():
    headers_gen = fake_headers.Headers(os="mac", browser="chrome")
    return headers_gen.generate()

parsed_data = []
for page in range(3):
    url = f'https://spb.hh.ru/search/vacancy?text=Python+django+flask&area=1&area=2&page={page}'
    main_response = requests.get(url, headers=gen_headers())
    main_html_data = main_response.text
    main_soup = BeautifulSoup(main_html_data, "lxml")


    for item in main_soup.find_all("div", class_="vacancy-serp-item__layout"):
        link_tag = item.find("a", class_="bloko-link")
        link = link_tag.get("href")
        vacancy = link_tag.find("span", class_="serp-item__title").text
        salary_tag = item.find("span", class_="bloko-header-section-2")
        salary = ""
        if salary_tag is not None:
            salary = " ".join(salary_tag.contents)
            salary = salary.replace("\u202f", " ")
        else:
            salary = "Зарплата не указана"
        company_tag = item.find("div", class_="bloko-v-spacing-container bloko-v-spacing-container_base-2")
        company = company_tag.find("div", class_="bloko-text").text
        company = company.replace("\xa0", " ")
        city = item.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text.split(",")[0]

        result = {
            "link": link,
            "vacancy": vacancy,
            "salary": salary,
            "company": company,
            "city": city
        }
        parsed_data.append(result)

pprint(parsed_data)

with open("vacancies_filtered.json", "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)

