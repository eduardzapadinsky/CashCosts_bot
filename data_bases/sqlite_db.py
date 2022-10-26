import datetime
import sqlite3 as sq

from create_bot import bot


def sql_start():
    """Створення таблиці"""
    global base, curs
    base = sq.connect('cash_costs.db')
    curs = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS cash_expenses(id INTEGER, goods TEXT, date TEXT, sum INTEGER)')
    base.commit()


async def sql_add(state):
    """Збереження витрат в БД"""
    async with state.proxy() as data:
        curs.execute('INSERT INTO cash_expenses VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_this_month(id):
    """Вивід витрат: за цей місяць"""
    stat_date = datetime.date.today().strftime("%Y-%m")
    expenses_sum = sql_statistics(id, stat_date)
    await bot.send_message(id, '\n'.join(expenses_sum), parse_mode='html')


async def sql_last_month(id):
    """Вивід витрат: за попередній місяць"""
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    stat_date = last_month.strftime("%Y-%m")
    expenses_sum = sql_statistics(id, stat_date)
    await bot.send_message(id, '\n'.join(expenses_sum), parse_mode='html')


async def sql_enter_period(data):
    """Вивід витрат: за вказаний період"""
    id = data["id"]
    period_start, period_finish = data["period"].replace(" ", '').split("-")
    period_start = datetime.datetime.strptime(period_start, '%d.%m.%y').date()
    period_finish = datetime.datetime.strptime(period_finish, '%d.%m.%y').date()
    stat_date = [period_start, period_finish]
    expenses_sum = sql_statistics(id, stat_date)
    await bot.send_message(id, '\n'.join(expenses_sum), parse_mode='html')


def sql_statistics(id, stat_date):
    """Вивід витрат: формування відповіді"""
    expenses = []
    for s in curs.execute('SELECT date, goods, sum FROM cash_expenses WHERE id == ?', (id,)).fetchall():
        expenses.append(s)
    expenses_sort = {}
    for dat, key, value in expenses:
        # Витрати за вказаний період
        if isinstance(stat_date, list):
            period_start, period_finish = stat_date
            dat_datetime = datetime.datetime.strptime(dat[:10], '%Y-%m-%d').date()
            if period_start <= dat_datetime <= period_finish:
                if key in expenses_sort:
                    expenses_sort[key].append(value)
                else:
                    expenses_sort[key] = [value]
        # Витрати за поточний та попередній місяць
        elif dat[:7] == stat_date:
            if key in expenses_sort:
                expenses_sort[key].append(value)
            else:
                expenses_sort[key] = [value]
    values_list = expenses_sort.values()
    # Розрахунок загальної суми витрат
    general_sum = sum([sum(i) for i in list(values_list)])
    # Формування відповіді
    expenses_sum = []
    for key, value in expenses_sort.items():
        value_sum = sum(value)
        expenses_sum.append(f"{key[1:]} <i>({round(100 * value_sum / general_sum)}%)</i> — <b>{value_sum}</b>")
    expenses_sum.append(f"—————")
    expenses_sum.append(f"<i>Total (100%)</i> — <b><u>{general_sum}</u></b>")
    return expenses_sum
