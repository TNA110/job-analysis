import requests
from itertools import count


languages = [
    "JavaScript",
    "Java",
    "Python",
    "Ruby",
    "PHP",
    "C++",
    "C#",
    "C",
]


def get_number_of_vacancies(language):
    url = f"https://api.hh.ru/vacancies?text=программист+{language}&area=1&"
    response = requests.get(url)
    response.raise_for_status()
    vacancies = response.json()
    vacancies_found = vacancies["found"]
    return vacancies_found

def predict_rub_salary(vacancy):
    salary =  vacancy["salary"]
    if salary:
        if salary["currency"]=="RUR":
            if salary["from"] and salary["to"]:
                predicted_salary = (int(salary["from"])+int(salary["to"]))/2
            elif salary["from"] and not salary["to"]:
                predicted_salary = 1.2 * int(salary["from"])
            elif salary["to"] and not salary["from"]:
                predicted_salary = 0.8 * int(salary["to"])
            return int(predicted_salary)
        else: None
    else: None

def get_all_vacancies(language):
    vacancies = []
    for page in count():
        #Ограничиваем количество страниц до 2000, т.к. API hh.ru предполагает глубину поиска 2000
        if page == 20:
            break
        params = {
            "area":"1",
            "page":f"{page}",
            "per_page":"100",
            }
        url = f"https://api.hh.ru/vacancies?text=программист%20{language}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies+=response.json().get("items")
    return vacancies

def get_all_vacancies_findings(): 
    all_vacancies_findings = []
    for language in languages:
        vacancies = get_all_vacancies(language)
        vacancies_processed = 0
        salaries_sum = 0
        for vacancy in vacancies:
            if predict_rub_salary(vacancy):
                salaries_sum = salaries_sum + predict_rub_salary(vacancy)
                vacancies_processed+=1 
            if not vacancies_processed==0:
                average_salary = int(salaries_sum/vacancies_processed)
            else: 
                None
        vacancy_findings = {
            language:{
                "vacancies_found":get_number_of_vacancies(language),
                "vacancies_processed":vacancies_processed,
                "average_salary":average_salary
                }
            }

        all_vacancies_findings.append(vacancy_findings)
    return all_vacancies_findings

