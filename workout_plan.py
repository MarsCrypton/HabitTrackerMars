from datetime import date, timedelta
plan = []

# Месяц 1: Привычка
for day in range(1, 31):
    push = 5 + (day - 1) * 1  # +1 каждый день
    squat = 5 + (day - 1) * 1
    plan.append((day, "отжимания", push, 1))
    plan.append((day, "приседания без веса", squat, 1))

# Месяц 2: Добавляем гантели и подходы
for day in range(31, 61):
    push = 10 + (day - 31)
    squat = 10 + (day - 31)
    row = 5 + (day - 31) * 0.5  # округляй вниз
    curl = 5 + (day - 31) * 0.5
    plan.append((day, "отжимания", push, 2))
    plan.append((day, "приседания без веса", squat, 2))
    plan.append((day, "тяга гантели в наклоне", int(row), 2))
    plan.append((day, "подъём гантели на бицепс", int(curl), 2))

# Месяц 3: Планка + длительность
for day in range(61, 92):
    push = 20 + (day - 61)
    squat = 20 + (day - 61)
    row = 10 + (day - 61)
    curl = 10 + (day - 61)
    plank = 20 + (day - 61)  # в секундах
    plan.append((day, "отжимания", push, 2))
    plan.append((day, "приседания без веса", squat, 2))
    plan.append((day, "тяга гантели в наклоне", row, 2))
    plan.append((day, "подъём гантели на бицепс", curl, 2))
    plan.append((day, "планка (в секундах)", plank, 1))

# Месяц 4: Добавляем румынскую тягу и ходьбу
for day in range(92, 123):
    push = 30 + (day - 92)
    squat = 30 + (day - 92)
    row = 15 + (day - 92)
    curl = 15 + (day - 92)
    deadlift = 10 + (day - 92)
    plank = 30 + (day - 92)
    walk = 10 + (day - 92)  # в минутах
    plan.append((day, "отжимания", push, 3))
    plan.append((day, "приседания без веса", squat, 3))
    plan.append((day, "тяга гантели в наклоне", row, 3))
    plan.append((day, "подъём гантели на бицепс", curl, 3))
    plan.append((day, "румынская тяга с гантелями", deadlift, 2))
    plan.append((day, "планка (в секундах)", plank, 1))
    plan.append((day, "бег на месте или на улице (в минутах)", walk, 1))

# Месяц 5: Увеличиваем объём
for day in range(123, 154):
    push = 40 + (day - 123)
    squat = 40 + (day - 123)
    row = 20 + (day - 123)
    curl = 20 + (day - 123)
    deadlift = 15 + (day - 123)
    plank = 40 + (day - 123)
    walk = 15 + (day - 123)
    plan.append((day, "отжимания", push, 3))
    plan.append((day, "приседания без веса", squat, 3))
    plan.append((day, "тяга гантели в наклоне", row, 3))
    plan.append((day, "подъём гантели на бицепс", curl, 3))
    plan.append((day, "румынская тяга с гантелями", deadlift, 3))
    plan.append((day, "планка (в секундах)", plank, 1))
    plan.append((day, "бег на месте или на улице (в минутах)", walk, 1))

# Месяц 6: Стабилизация привычки
for day in range(154, 185):
    push = 50
    squat = 50
    row = 25
    curl = 25
    deadlift = 20
    plank = 60
    walk = 20
    plan.append((day, "отжимания", push, 3))
    plan.append((day, "приседания без веса", squat, 3))
    plan.append((day, "тяга гантели в наклоне", row, 3))
    plan.append((day, "подъём гантели на бицепс", curl, 3))
    plan.append((day, "румынская тяга с гантелями", deadlift, 3))
    plan.append((day, "планка (в секундах)", plank, 1))
    plan.append((day, "бег на месте или на улице (в минутах)", walk, 1))


