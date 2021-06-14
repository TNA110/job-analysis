from terminaltables import AsciiTable


def build_vacancies_table(table_title, site_vacancies):
    table_data = (
        ("Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"),
    )
    for language_vacancy in site_vacancies:
        language = list(language_vacancy.keys())[0]
        vacancies_found = language_vacancy[f"{language}"].get("vacancies_found")
        vacancies_processed = language_vacancy[f"{language}"].get("vacancies_processed")
        average_salary = language_vacancy[f"{language}"].get("average_salary")
        table_string = (
            f"{language}", 
            f"{vacancies_found}",
            f"{vacancies_processed}",
            f"{average_salary}"
        )
        table_data = table_data + (table_string,)
        
    table_instance = AsciiTable(table_data, table_title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)