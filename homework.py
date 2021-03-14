import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(rec.amount for rec in self.records if rec.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        amount_for_7_days = dt.date.today() - dt.timedelta(days=7)
        return sum(week_date.amount for week_date in self.records
                   if amount_for_7_days <= week_date.date <= today)

    def ostatok_na_day(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 60.44
    EURO_RATE = 80.88
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        if self.ostatok_na_day() == 0:
            return 'Денег нет, держись'

        dict_rate = {
            'rub': ('руб', CashCalculator.RUB_RATE),
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE)
        }
        if currency not in dict_rate:
            raise ValueError('Ошибка ввода валюты. Введите одну из: '
                             '"rub", "usd" или "eur" !')
        currency_rate, currency_name = dict_rate[currency]
        stat_today = self.get_today_stats()
        stat_rate = self.get_today_stats() / currency_name
        stat_limit = self.limit / currency_name

        if self.limit > stat_today:
            can_spend = round(stat_limit - stat_rate, 2)
            return f'На сегодня осталось {can_spend} {currency_rate}'

        not_can_spend = round(stat_rate - stat_limit, 2)
        return (
                'Денег нет, держись: твой '
                f'долг - {not_can_spend} {currency_rate}'
            )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.ostatok_na_day() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.ostatok_na_day()} кКал')
        return 'Хватит есть!'
