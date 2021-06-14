import requests
from itertools import count
import dotenv
import os


dotenv.load_dotenv()

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
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id":os.getenv("SUPERJOB_APP_ID")}
    params = {"town":"4", "catalogues":"48", "keyword":f"{language}"}
    response = requests.get(url, headers=headers, params = params)
    response.raise_for_status()
    vacancies = response.json()
    vacancies_found = vacancies["total"]
    return vacancies_found

def predict_rub_salary(vacancy):
    predicted_salary = None
    if vacancy["currency"]=="rub":
        if vacancy["payment_from"]!=0 and vacancy["payment_to"]!=0:
            predicted_salary = (int(vacancy["payment_from"])+int(vacancy["payment_to"]))/2
        elif vacancy["payment_from"]!=0 and vacancy["payment_to"]==0:
            predicted_salary = 1.2 * int(vacancy["payment_from"])
        elif vacancy["payment_to"]!=0 and vacancy["payment_from"]==0:
            predicted_salary = 0.8 * int(vacancy["payment_to"])
    if predicted_salary:
        return int(predicted_salary)
    else: None
      
def get_all_vacancies(language):
    vacancies = []
    for page in count(0):
        if page == 5:
            break
        url = f"https://api.superjob.ru/2.0/vacancies/"
        headers = {"X-Api-App-Id":"v3.h.4115001.5f33d302f6bcae9d13cdd5a2c48a4c7dbf5b2f09.57ec80a7e04344a41f0ed7a900cd2396aa45c30a"}
        params = {"town":"4", "catalogues":"48", "keyword":f"{language}", "page":f"{page}", "count":"100"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies+=response.json().get("objects")
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

