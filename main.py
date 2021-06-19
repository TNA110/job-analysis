import fetch_headhunter
import fetch_superjob
import build_table
import dotenv
import requests


def main():
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

    headhunter_vacancies = fetch_headhunter.get_all_vacancies_findings(languages)
    superjob_vacancies = fetch_superjob.get_all_vacancies_findings(languages)

    table_entries = (
        ("Headhunter Mocsow", headhunter_vacancies),
        ("SuperJob Moscow", superjob_vacancies),
    )

    for site_table_entry in table_entries:
        table_title, site_vacancies = site_table_entry
        build_table.build_vacancies_table(table_title, site_vacancies)


if __name__ == "__main__":
    main()
