def predict_rub_salary(salary_from, salary_to):
    predicted_salary = None
    if salary_from and salary_to:
        predicted_salary = (int(salary_from)+int(salary_to))/2
    elif salary_from and not salary_to:
        predicted_salary = 1.2 * int(salary_from)
    elif salary_to and not salary_from:
        predicted_salary = 0.8 * int(salary_to)
    if predicted_salary:
        return int(predicted_salary)
