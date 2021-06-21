from terminaltables import AsciiTable


def build_vacancies_table(table_title, site_vacancies):
    table_data = (
        ("Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"),
    )
    for language_vacancies in site_vacancies.items():
        language, vacancies_findings = language_vacancies
        vacancies_found = vacancies_findings.get("vacancies_found")
        vacancies_processed = vacancies_findings.get("vacancies_processed")
        average_salary = vacancies_findings.get("average_salary")
        table_string = (
            f"{language}",
            f"{vacancies_found}",
            f"{vacancies_processed}",
            f"{average_salary}"
        )
        table_data = table_data + (table_string,)
    table_instance = AsciiTable(table_data, table_title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
