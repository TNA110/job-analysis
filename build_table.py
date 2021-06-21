from terminaltables import AsciiTable


def build_vacancies_table(table_title, site_vacancies):
    table_content = (
        ("Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"),
    )
    for language, vacancies_findings in site_vacancies.items():
        table_string = (
            language,
            vacancies_findings.get("vacancies_found"),
            vacancies_findings.get("vacancies_processed"),
            vacancies_findings.get("average_salary")
        )
        table_content = table_content + (table_string,)
    table_instance = AsciiTable(table_content, table_title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
