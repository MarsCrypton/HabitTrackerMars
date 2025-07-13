import json
from datetime import date
import os

class Habit:
    def __init__(self, name):
        self.name = name
        self.days_completed = []

    def mark_today(self):
        today = str(date.today())
        if today not in self.days_completed:
            self.days_completed.append(today)

    def progress(self):
        return len(self.days_completed)

    def __str__(self):
        return f"{self.name}: выполнено {self.progress()} раз(а)"
    

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
    

