from datetime import date, datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
    # Реалізуйте тут домашнє завдання
    users_list = defaultdict(list)
    # Cuurent date
    today_date = date.today()
    # Current year
    current_year = today_date.year

    week_interval = timedelta(days=7)

    if len(users) < 1:
        return {}
    
    for dictionary in users:
        user_birthday = dictionary.get("birthday")

        if user_birthday.month == 1:
            user_birthday = user_birthday.replace(year=current_year + 1)
        else:
            user_birthday = user_birthday.replace(year=current_year)

        if (user_birthday - today_date > week_interval) or (user_birthday < today_date):
            continue
        
        birthday_weekday = user_birthday.weekday()

        if birthday_weekday not in (5, 6):
            users_list[user_birthday.strftime('%A')].append(dictionary.get("name"))
        else:
            users_list["Monday"].append(dictionary.get("name"))

    return users_list


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")

