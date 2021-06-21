import requests
from itertools import count
import os
import predict_salary

SUPERJOB_APP_ID = os.getenv("SUPERJOB_APP_ID")
moscow_id = "4"
programmers_catalogues_id = "48"


def get_all_vacancies(language):
    vacancies = []
    headers = {"X-Api-App-Id": SUPERJOB_APP_ID}
    params = {
        "town": moscow_id,
        "catalogues": programmers_catalogues_id,
        "keyword": language,
        "page": None,
        "count": "100"
    }
    for page in count(0):
        params.update(page=page)
        url = "https://api.superjob.ru/2.0/vacancies/"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies_response = response.json()
        vacancies += vacancies_response.get("objects")
        if not vacancies_response.get("more"):
            break
    vacancies_found = vacancies_response.get("total")
    return vacancies, vacancies_found


def get_all_vacancies_findings(languages):
    all_vacancies_findings = {}
    for language in languages:
        vacancies, vacancies_found = get_all_vacancies(language)
        vacancies_processed = 0
        salaries_sum = 0
        average_salary = 0
        for vacancy in vacancies:
            if not vacancy["currency"] == "rub":
                continue
            predicted_salary = predict_salary.predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"])
            if not predicted_salary:
                continue
            salaries_sum += predicted_salary
            vacancies_processed += 1
        if vacancies_processed:
            average_salary = int(salaries_sum/vacancies_processed)
        vacancy_findings = {
                "vacancies_found": vacancies_found,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
            }

        all_vacancies_findings[language] = vacancy_findings
    return all_vacancies_findings
