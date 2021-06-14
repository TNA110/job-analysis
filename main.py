import fetch_headhunter, fetch_superjob, build_table


headhunter_vacancies = fetch_headhunter.get_all_vacancies_findings()
superjob_vacancies = fetch_superjob.get_all_vacancies_findings()

table_entries = (
    ("Headhunter Mocsow", headhunter_vacancies),
    ("SuperJob Moscow", superjob_vacancies),
)

for site_table_entry in table_entries:
    table_title, site_vacancies = site_table_entry
    build_table.build_vacancies_table(table_title, site_vacancies)
