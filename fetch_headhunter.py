import requests
from itertools import count
import predict_salary


def get_all_vacancies(language):
    vacancies = []
    for page in count():
        params = {
            "area": "1",
            "page": f"{page}",
            "per_page": "100",
            "text": f"программист {language}"
            }
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
            vacancies_found = response.json().get("found")
        except requests.exceptions.HTTPError:
            if response.status_code == 400:
                break
            else:
                raise
        vacancies += response.json().get("items")
    return (vacancies, vacancies_found)


def get_all_vacancies_findings(languages):
    all_vacancies_findings = []
    for language in languages:
        vacancies, vacancies_found = get_all_vacancies(language)
        vacancies_processed = 0
        salaries_sum = 0
        for vacancy in vacancies:
            salary = vacancy["salary"]
            try:
                if salary["currency"] == "RUR":
                    predicted_salary = predict_salary.predict_rub_salary(salary["from"], salary["to"])
                    if predicted_salary:
                        salaries_sum += predicted_salary
                        vacancies_processed += 1
                    if vacancies_processed:
                        average_salary = int(salaries_sum/vacancies_processed)
            except TypeError:
                pass

        vacancy_findings = {
            language: {
                "vacancies_found": vacancies_found,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
                }
            }

        all_vacancies_findings.append(vacancy_findings)
    return all_vacancies_findings
