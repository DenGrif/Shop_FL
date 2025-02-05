# shop/management/commands/create_products.py
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Create sample products for the catalog'

    def handle(self, *args, **kwargs):
        products = [
            {'name': 'Роза', 'description': 'Красная роза', 'price': 500, 'category': 'flower'},
            {'name': 'Тюльпан', 'description': 'Желтый тюльпан', 'price': 350, 'category': 'flower'},
            {'name': 'Лилия', 'description': 'Белая лилия', 'price': 600, 'category': 'flower'},
            {'name': 'Букет №1', 'description': 'Состав: розы, тюльпаны, лилии', 'price': 2000, 'category': 'bouquet'},
            {'name': 'Букет №2', 'description': 'Состав: хризантемы, ирисы', 'price': 1500, 'category': 'bouquet'},
            {'name': 'Гербера', 'description': 'Оранжевая гербера', 'price': 400, 'category': 'flower'},
            {'name': 'Пионы', 'description': 'Пионы с приятным запахом', 'price': 700, 'category': 'flower'},
            {'name': 'Орхидея фаленопсис', 'description': 'Белая орхидея в горшке', 'price': 1200,
             'category': 'flower'},
            {'name': 'Букет "Нежность"', 'description': 'Пионы, эустомы и гипсофила', 'price': 3500,
             'category': 'bouquet'},
            {'name': 'Хризантема кустовая', 'description': 'Бордовая, 5 веток', 'price': 850, 'category': 'flower'},
            {'name': 'Свадебный букет', 'description': 'Белые розы и гортензии', 'price': 4500, 'category': 'bouquet'},
            {'name': 'Ирис голландский', 'description': 'Фиолетовые ирисы, 7 шт', 'price': 600, 'category': 'flower'},
            {'name': 'Корзина "Осенний вальс"', 'description': 'Хризантемы, герберы, декоративные тыквы', 'price': 2800,
             'category': 'bouquet'},
            {'name': 'Эустома', 'description': 'Розовые махровые эустомы', 'price': 750, 'category': 'flower'},
            {'name': 'Букет для мужчины', 'description': 'Антуриумы, зелень в строгой упаковке', 'price': 3200,
             'category': 'bouquet'},
            {'name': 'Гортензия', 'description': 'Голубая гортензия в срезке', 'price': 900, 'category': 'flower'},
            {'name': 'Мимоза', 'description': 'Пушистые ветки мимозы к 8 марта', 'price': 400, 'category': 'flower'},
            {'name': 'Букет "Прованс"', 'description': 'Лаванда, розы и полевые цветы', 'price': 2700,
             'category': 'bouquet'},
            {'name': 'Альстромерия', 'description': 'Смесь окрасок, 10 стеблей', 'price': 650, 'category': 'flower'},
            {'name': 'Шляпная коробка "Люкс"', 'description': 'Розы, пионы и эвкалипт', 'price': 5000,
             'category': 'bouquet'},
            {'name': 'Гиацинт', 'description': 'Ароматные белые гиацинты в горшке', 'price': 550, 'category': 'flower'},
            {'name': 'Букет "Императорский"', 'description': 'Каллы, орхидеи и ветки сакуры', 'price': 6800,
             'category': 'bouquet'},
            {'name': 'Фрезия', 'description': 'Разноцветные фрезии, 15 стеблей', 'price': 950, 'category': 'flower'},
            {'name': 'Новогодняя композиция', 'description': 'Хвоя, красные розы, шишки и свеча', 'price': 4200,
             'category': 'bouquet'},
        ]

        for product_data in products:
            Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('Successfully created products'))
