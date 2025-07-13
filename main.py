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
        print("4. Удалить привычку")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Название привычки: ")
            tracker.add_habit(name)

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
            except ValueError:
                print("Нужно ввести число.")


        elif choice == "0":
            tracker.save_to_file(FILENAME)
            print("Привычки сохранены. Выход...")
            break

        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()
