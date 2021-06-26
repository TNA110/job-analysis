
from itertools import count

import requests

import predict_salary


MOSCOW_ID = "4"
PROGRAMMERS_CATALOGUES_ID = "48"


def get_all_vacancies(language, superjob_app_id):
    vacancies = []
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": superjob_app_id}
    params = {
        "town": MOSCOW_ID,
        "catalogues": PROGRAMMERS_CATALOGUES_ID,
        "keyword": language,
        "count": "100"
    }
    for page in count(0):
        params.update(page=page)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies_response = response.json()
        vacancies += vacancies_response.get("objects")
        if not vacancies_response.get("more"):
            break
    vacancies_found = vacancies_response.get("total")
    return vacancies, vacancies_found


def collect_language_stats(language, superjob_app_id):
    vacancies, vacancies_found = get_all_vacancies(language, superjob_app_id)
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
    return vacancies_found, vacancies_processed, average_salary


def get_all_vacancies_findings(languages, superjob_app_id):
    all_vacancies_findings = {}
    for language in languages:
        vacancies_found, vacancies_processed, average_salary = collect_language_stats(language, superjob_app_id)
        all_vacancies_findings[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return all_vacancies_findings
