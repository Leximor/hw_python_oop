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


class CashCalculator(Calculator):
    USD_RATE = 60.44
    EURO_RATE = 80.88
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        self.currency = currency
        dict_rate = {
            'rub': ['руб', CashCalculator.RUB_RATE],
            'usd': ['USD', CashCalculator.USD_RATE],
            'eur': ['Euro', CashCalculator.EURO_RATE]
        }
        stat_today = self.get_today_stats()
        if self.limit == stat_today:
            return 'Денег нет, держись'
        elif self.limit > stat_today:
            can_spend = round(self.limit / dict_rate[currency][1]
                              - stat_today / dict_rate[currency][1], 2)
            return f'На сегодня осталось {can_spend} {dict_rate[currency][0]}'
        else:
            not_can_spend = round(stat_today / dict_rate[currency][1]
                                  - self.limit / dict_rate[currency][1], 2)
            return (
                'Денег нет, держись: твой '
                f'долг - {not_can_spend} {dict_rate[currency][0]}'
            )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        ostatok_today_calories = self.limit - self.get_today_stats()
        if ostatok_today_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{ostatok_today_calories} кКал')
        return 'Хватит есть!'
