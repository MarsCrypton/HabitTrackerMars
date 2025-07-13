from habit import HabitTracker

FILENAME = "data.json"

def main():
    tracker = HabitTracker()
    tracker.load_from_file(FILENAME)

    while True:
        print("\n=== Трекер Привычек ===")
        print("1. Добавить привычку")
        print("2. Отметить выполнение")
        print("3. Показать прогресс")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Название привычки: ")
            tracker.add_habit(name)

        elif choice == "2":
            name = input("Какая привычка выполнена?: ")
            habit = tracker.find_habit(name)
            if habit:
                habit.mark_today()
                print("Отмечено!")
            else:
                print("Привычка не найдена.")

        elif choice == "3":
            tracker.show_all()

        elif choice == "0":
            tracker.save_to_file(FILENAME)
            print("Привычки сохранены. Выход...")
            break

        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()
