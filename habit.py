import json
from datetime import date
import os

class Habit:
    def __init__(self, name, days_completed=None):
        self.name = name
        self.days_completed = days_completed if days_completed else []

    def mark_today(self):
        today = str(date.today())
        if today not in self.days_completed:
            self.days_completed.append(today)

    def progress(self):
        return len(self.days_completed)

    def __str__(self):
        return f"{self.name}: выполнено {self.progress()} раз(а)"
    
    def to_dict(self):
        return {"name": self.name, "days_completed": self.days_completed}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["days_completed"])
    

class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, name):
        if self.find_habit(name):
            print("Привычка уже существует.")
        else:
            self.habits.append(Habit(name))

    def find_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                return habit
        return None

    def show_all(self):
        if not self.habits:
            print("Нет привычек.")
        for habit in self.habits:
            print(habit)

    def save_to_file(self, filename):
        data = [habit.to_dict() for habit in self.habits]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filename):
        if not os.path.exists(filename):
            return  # Ничего не загружаем, если файл не существует
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.habits = [Habit.from_dict(item) for item in data]

    def remove_habit_by_index(self, index):
        if 0 <= index < len(self.habits):
            removed = self.habits.pop(index)
            print(f"Привычка '{removed.name}' удалена.")
        else:
            print("Неверный номер.")

