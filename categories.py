# categories = {"1": "Харчування", "2": "Транспорт", "3": "Будинок", "4": "Здоровʼя", "5": "Подарунки", "6": "Послуги",
#               "7": "Одяг", "8": "Інше"}
#
statistics = {'2': 'день',
              '3': 'тиждень',
              '4': 'місяць',
              '5': 'рік',
              }
import database


class Category:

    def __init__(self, category):
        self.id: int
        self.category: str = category


class Categories:
    def __init__(self):
        self._categories = self._get_all_categories()

    @property
    def category_id(self):
        return self._get_one_category()

    @property
    def all_categories(self):
        return self._categories

    @staticmethod
    def _get_all_categories() -> dict:
        """Return all categories from DB"""
        categories = database.fetchall("Categories", "id", "name_ua")
        return categories

    @staticmethod
    def _get_one_category():
        """"return one category"""
        # TBD

        category_id = None
        return category_id
