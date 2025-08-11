from habit import HabitTracker
from meals import MEAL_PLAN, parse_meal_line, parse_meal_line_tomorrow,print_meal_table
from datetime import date, timedelta

from workout_plan import plan

from rich.console import Console
from rich.table import Table
console = Console()

FILENAME = "data.json"

# ----------  Вспомогательная дата старта ----------
START_DATE = date(2025, 8, 12)  

def main():
    while True:
        console.print('[orange1]-----------------------------------------------------------------------------------------------[/orange1]')
        console.print("\n[orange1]=== Главное меню ===[/orange1]")
        print("1. Сводка на сегодня")
        print("2. Трекер привычек")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            today()

        elif choice == "2":
            habit_menu()
        
        elif choice == "0":
            print("Выход...")
            break

        else:
            print("Неверный ввод.")

def habit_menu():
    tracker = HabitTracker()
    tracker.load_from_file(FILENAME)

    while True:
        console.print("\n[orange1]=== Трекер Привычек ===[/orange1]")
        print("1. Добавить привычку")
        print("2. Отметить выполнение")
        print("3. Показать прогресс")
        print("4. Удалить привычку")
        print("5. Архивировать привычку")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Название привычки: ")
            while True:
                x = input("Цель (выполнений, например 10): ").strip()
                if x == "":
                    goal = None  # пользователь не задал цель
                    break
                try:
                    goal = int(x)
                    break
                except ValueError:
                    print("Ошибка: введите число или оставьте поле пустым.")

            tracker.add_habit(name, goal)
            tracker.save_to_file(FILENAME)

        elif choice == "2":
            if not tracker.habits:
                print("Нет привычек для выполнения.")
                continue

            print("Список привычек:")
            for i, habit in enumerate(tracker.habits):
                print(f"{i + 1}. {habit.name}")
            try:
                idx = int(input("Введите номер привычки для выполнения: ")) - 1
                tracker.mark_today(idx)
                tracker.save_to_file(FILENAME)
            except ValueError:
                print("Нужно ввести число.")

        elif choice == "3":
            tracker.show_all()

        elif choice == "4":
            if not tracker.habits:
                print("Нет привычек для удаления.")
                continue

            print("Список привычек:")
            for i, habit in enumerate(tracker.habits):
                print(f"{i + 1}. {habit.name}")

            try:
                idx = int(input("Введите номер привычки для удаления: ")) - 1
                tracker.remove_habit_by_index(idx)
                tracker.save_to_file(FILENAME)
            except ValueError:
                print("Нужно ввести число.")

        elif choice == "5":
            print("Список привычек:")
            active = [h for h in tracker.habits if not h.is_archived]
            for i, habit in enumerate(active):
                print(f"{i + 1}. {habit.name}")
            try:
                idx = int(input("Введите номер привычки для архивирования: ")) - 1
                tracker.archive_habit_by_index(idx)
                tracker.save_to_file(FILENAME)
            except ValueError:
                print("Нужно ввести число.")
    


        elif choice == "0":
            tracker.save_to_file(FILENAME)
            print("\nПривычки сохранены. Возврат в главное меню")
            break

        else:
            print("\nНеверный ввод.")

def today():
    today = date.today()
    day_of_month = today.day
    day_today   = (today - START_DATE).days + 1
    day_tomorrow = day_today + 1
    

    tracker = HabitTracker()
    tracker.load_from_file(FILENAME)

    breakfast, lunch, dinner = parse_meal_line()
    tomorrow_breakfast,tomorrow_lunch,tomorrow_dinner = parse_meal_line_tomorrow()

    if not MEAL_PLAN:
        print("\nФайл пуст или не найден!")

    elif day_of_month > len(MEAL_PLAN):
        print("\nМеню не задано на этот день")

    

    else:
        console.print('[orange1]-----------------------------------------------------------------------------------------------[/orange1]')
        print_meal_table(
            breakfast, lunch, dinner,
            tomorrow_breakfast, tomorrow_lunch, tomorrow_dinner
        )
        console.print("[orange1]Прогресс привычек[/orange1]")
        tracker.show_all_1()



        console.print(f"\n[orange1]Спорт на сегодня (день {day_today}):[/orange1]")
        if 1 <= day_today <= len(plan):
            for d, ex, reps, sets in plan:
                if d == day_today:
                    print(f"  • {ex}: {reps} повт × {sets} подх")
                    console.print('[orange1]-----------------------------------------------------------------------------------------------[/orange1]')
                    
        else:
            print("  Программа завершена!")

        console.print(f"\n[orange1]Спорт на завтра (день {day_tomorrow}):[/orange1]")
        if 1 <= day_tomorrow <= len(plan):
            for d, ex, reps, sets in plan:
                if d == day_tomorrow:
                    print(f"  • {ex}: {reps} повт × {sets} подх")
        else:
            print("  Программа завершена!")
        

if __name__ == "__main__":
    main()
