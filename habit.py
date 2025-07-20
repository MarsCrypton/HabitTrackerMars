import json
from datetime import date,datetime, timedelta
import os

class Habit:
    def __init__(self, name, days_completed=None, goal=None):
        self.name = name
        self.goal = goal
        self.days_completed = days_completed if days_completed else []

    def is_goal_reached(self):
        if self.goal is None:
            return False
        return self.progress() >= self.goal

    def mark_today(self):
        today = str(date.today())
        if today not in self.days_completed:
            self.days_completed.append(today)

    def progress(self):
        return len(self.days_completed)

    def get_best_streak(self):
        if not self.days_completed:
            return (0, None, None)
        dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in self.days_completed])
        dates.sort()

        best_start = best_end = current_start = dates[0]
        best_len = current_len = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current_len += 1
                current_end = dates[i]
            else:
                if current_len > best_len:
                    best_len = current_len
                    best_start = current_start
                    best_end = dates[i - 1]
                current_len = 1
                current_start = dates[i]
        if current_len > best_len:
            best_len = current_len
            best_start = current_start
            best_end = dates[-1]

        return (best_len, best_start, best_end)


    def __str__(self):
        if self.goal is None:
            goal_status = "цель: не задана"
        elif self.is_goal_reached():
            goal_status = f"цель: {self.goal} ✅ достигнута!"
        else:
            x = self.goal - self.progress()
            goal_status = f"цель: {self.goal} (осталось {x})"


        if self.days_completed:
            dates = "\n  - " + "\n  - ".join(self.days_completed)
        else:
                dates = "\n  (пока нет выполнений)"
                
        streak_len, streak_start, streak_end = self.get_best_streak()
        if streak_len ==0:
            streak_info = "📈 Стрик: пока нет подряд выполнений"
        else:
            streak_info = f"📈 Стрик: {streak_len} дней (с {streak_start} по {streak_end})"

        return f"\n{self.name}: выполнено {self.progress()} раз(а) / цель: {goal_status}\n{streak_info}"

    
    def to_dict(self):
        return {"name": self.name, "days_completed": self.days_completed,"goal":self.goal}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["days_completed"],data["goal"])
    

class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, name, goal=None):
        if self.find_habit(name):
            print("Привычка уже существует.")
        else:
            self.habits.append(Habit(name, goal=goal))

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
        if os.path.getsize(filename) == 0:
            return  # файл пустой — ничего не загружаем
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.habits = [Habit.from_dict(item) for item in data]

    def remove_habit_by_index(self, index):
        if 0 <= index < len(self.habits):
            removed = self.habits.pop(index)
            print(f"Привычка '{removed.name}' удалена.")
        else:
            print("Неверный номер.")

    def mark_today(self, index):
        if 0 <= index < len(self.habits):
            habit = self.habits[index]
            habit.mark_today()
            print(f"Привычка '{habit.name}' отмечена!")
        else:
            print("Неверный номер.")

