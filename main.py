from habit import HabitTracker
from meals import MEAL_PLAN
from datetime import date

from rich.console import Console
console = Console()

FILENAME = "data.json"

def main():
    while True:
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
    meals = MEAL_PLAN

    tracker = HabitTracker()
    tracker.load_from_file(FILENAME)

    if not meals:
        print("\nФайл пуст или не найден!")

    elif day_of_month > len(meals):
        print("\nМеню не задано на этот день")

    else:
        console.print(f"\n[orange1]Меню на {today.strftime('%d.%m.%Y')}:[/orange1]\n{(meals[(day_of_month)-1])}\n")
        tracker.show_all_1()
        
        # print(meals[(day_of_month)-1])

if __name__ == "__main__":
    main()
