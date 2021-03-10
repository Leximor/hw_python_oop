import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = (dt.datetime.strptime(date, '%d.%m.%Y')).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        amount_now = 0
        for rec in self.records:
            if rec.date == dt.date.today():
                amount_now += rec.amount
        return amount_now

    def get_week_stats(self):
        week_amount = 0
        week_amount_for_7_days = dt.date.today() - dt.timedelta(days=7)
        for week_date in self.records:
            if week_amount_for_7_days <= week_date.date <= dt.date.today():
                week_amount += week_date.amount
        return week_amount


class CashCalculator(Calculator):
    USD_RATE = 60.44
    EURO_RATE = 80.88

    def get_today_cash_remained(self, currency):
        self.currency = currency
        if self.currency == "rub":
            cash_sell = round(self.limit - self.get_today_stats(), 2)
            val = "руб"
        elif self.currency == "usd":
            cash_sell = round((self.limit / CashCalculator.USD_RATE
                               - self.get_today_stats()
                               / CashCalculator.USD_RATE), 2)
            val = "USD"
        elif self.currency == "eur":
            cash_sell = round((self.limit / CashCalculator.EURO_RATE
                               - self.get_today_stats()
                               / CashCalculator.EURO_RATE), 2)
            val = "Euro"
        if cash_sell > 0:
            return (f'На сегодня осталось {cash_sell} {val}')
        elif cash_sell == 0:
            return ('Денег нет, держись')
        else:
            return (f'Денег нет, держись: твой долг - {abs(cash_sell)} {val}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        ostatok_today_calories = self.limit - self.get_today_stats()
        if ostatok_today_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{ostatok_today_calories} кКал')
        else:
            return ('Хватит есть!')
