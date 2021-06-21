def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif salary_from and not salary_to:
        return int(1.2 * salary_from)
    elif salary_to and not salary_from:
        return int(0.8 * salary_to)
