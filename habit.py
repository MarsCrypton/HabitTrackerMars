import json
from datetime import date, datetime, timedelta
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress
from rich.progress_bar import ProgressBar
from rich.progress import Progress, BarColumn, TextColumn
console = Console()

class Habit:
    def __init__(self, name, days_completed=None, goal=None, is_archived=False):
        self.name = name
        self.goal = goal
        self.days_completed = days_completed if days_completed else []
        self.is_archived = is_archived

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
                # current_end = dates[i]
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

    def get_current_streak(self):
        if not self.days_completed:
            return (0, None)
        else:
            dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in self.days_completed], reverse=True)
            today = date.today()
            streak = 0 
            for d in dates:
                if d == today - timedelta(days=streak):
                    streak += 1
                else:
                    break

        if streak > 0:
            start_date = today - timedelta(days=streak - 1)
            return (streak, start_date)
        else:
            return (0, None)

    def archive_habit_by_index(self, index):
        active = [h for h in self.habits if not h.is_archived]
        if 0 <= index < len(active):
            habit = active[index]
            if habit.is_goal_reached():
                habit.is_archived = True
                print(f"Привычка '{habit.name}' архивирована.")
                return True 
            else:
                print("Цель ещё не достигнута. Нельзя архивировать.")
        else:
            print("Неверный номер.")

    def display_rich(self):
        if self.progress() == 0:
            console.print(f"[dim]{self.name}[/dim]: [red]0%[/red]")
        else:
            with Progress("[progress.description]{task.description}",
                BarColumn(complete_style="green", finished_style="cyan", pulse_style="none"),
                TextColumn("[green]{task.percentage:>3.0f}%[/green]"),
            )as progress:
                task_id = progress.add_task(f"{self.name}", total=self.goal)
                progress.update(task_id, completed=self.progress())


    def __str__(self):
        if self.goal is None:
            goal_status = "цель: не задана"
        elif self.is_goal_reached():
            goal_status = f"цель: {self.goal} ✅ достигнута!"
        else:
            x = self.goal - self.progress()
            goal_status = f"цель: {self.goal} (осталось {x})"

        # progress_bar = ""
        # if self.goal and self.goal > 0:
        #     bar_length  = 50
        #     filled = int((self.progress() / self.goal)* bar_length )
        #     empty = bar_length  - filled
        #     progress_bar = f"\n📊 Прогресс: [{'█' * filled}{'░' * empty}] {self.progress()}/{self.goal}"



        if self.days_completed:
            dates = "\n  - " + "\n  - ".join(self.days_completed)
        else:
            dates = "\n  (пока нет выполнений)"
                
        streak_len, streak_start, streak_end = self.get_best_streak()
        current_len, current_start = self.get_current_streak()

        if current_len == 0:
            current_info = "Текущий стрик: прерван"
        else:
            current_info = f"Текущий стрик: {current_len} дней (с {current_start})"

        if streak_len == 0:
            streak_info = "Стрик: пока нет подряд выполнений"
        else:
            streak_info = f"Стрик: {streak_len} дней (с {streak_start} по {streak_end})"

        return f"""Выполнено {self.progress()} раз(а) / цель: {goal_status}\n{streak_info}\n{current_info}\n"""
    
    def to_dict(self):
        return {
            "name": self.name,
            "days_completed": self.days_completed,
            "goal":self.goal,
            "is_archived": self.is_archived
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data.get("days_completed", []),
            data.get("goal"),
            data.get("is_archived",False)
        )
    
    
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
        active = [h for h in self.habits if not h.is_archived]
        if not active:
            print("Нет активных привычек.")
        for habit in active:
            habit.display_rich()
            print(habit)

    def show_all_1(self):
        active = [h for h in self.habits if not h.is_archived]
        if not active:
            print("Нет активных привычек.")
        for habit in active:
            habit.display_rich()


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

    def archive_habit_by_index(self, index):
        active = [h for h in self.habits if not h.is_archived]
        if 0 <= index < len(active):
            habit = active[index]
            if habit.is_goal_reached():
                habit.is_archived = True
                print(f"Привычка '{habit.name}' архивирована.")
                return True 
            else:
                print("Цель ещё не достигнута. Нельзя архивировать.")
        else:
            print("Неверный номер.")

