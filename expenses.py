import database
from datetime import datetime


def get_day_expenses():
    pass


def get_week_expenses():
    pass


def get_month_expenses():
    pass


def get_year_expenses():
    pass


def add_expense(category_id, category_name_ua, user_id, amount):
    """id               integer primary key not null,
    category_id      integer,
    category_name_ua varchar(255),
    user_id          integer,
    amount           float,
    date """
    date = datetime.now()
    column_values = {}
    database.insert('Expenses', column_values)
