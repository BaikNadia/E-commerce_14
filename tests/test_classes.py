import pytest

from src.classes import Category, Product, Smartphone, LawnGrass


# === Фикстура для сброса счётчиков перед каждым тестом ===
@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0


# === Тесты ===
def test_product_initialization():
    """Проверяет инициализацию объекта Product"""
    product = Product("Ноутбук", "Мощный ноутбук", 99999.99, 5)
    assert product.name == "Ноутбук"
    assert product.description == "Мощный ноутбук"
    assert product.price == 99999.99
    assert product.quantity == 5


def test_category_initialization_without_products():
    """Проверяет инициализацию категории без продуктов"""
    category = Category("Электроника", "Различные электронные устройства")
    assert category.name == "Электроника"
    assert category.description == "Различные электронные устройства"
    assert len(category.products) == 0


def test_category_initialization_with_products():
    """Проверяет инициализацию категории с продуктами"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Планшет", "Сенсорный экран", 30000.0, 5)
    category = Category("Гаджеты", "Мобильные устройства", [product1, product2])

    assert category.name == "Гаджеты"
    assert category.description == "Мобильные устройства"
    assert len(category.products) == 2

    # Проверяем наличие строк в нужном формате
    expected_product1 = "Телефон, 50000 руб. Остаток: 10 шт."
    expected_product2 = "Планшет, 30000 руб. Остаток: 5 шт."

    assert expected_product1 in category.products
    assert expected_product2 in category.products


def test_category_count():
    """Проверяет подсчёт общего количества категорий"""
    Category("Категория 1", "Описание 1")
    Category("Категория 2", "Описание 2")
    assert Category.category_count == 2


def test_product_count_initialization():
    """Проверяет подсчёт продуктов при инициализации"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Планшет", "Сенсорный экран", 30000.0, 5)
    Category("Гаджеты", "Мобильные устройства", [product1, product2])
    assert Category.product_count == 2


def test_product_count_multiple_categories():
    """Проверяет общий подсчёт продуктов в нескольких категориях"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Планшет", "Сенсорный экран", 30000.0, 5)
    product3 = Product("Ноутбук", "Мощный ноутбук", 99999.99, 5)

    Category("Гаджеты", "Мобильные устройства", [product1, product2])
    Category("Компьютеры", "Стационарные устройства", [product3])

    assert Category.product_count == 3


# === Тесты для класса Product ===
def test_product_initialization_with_positive_price():
    product = Product("Ноутбук", "Мощный", 99999.99, 5)
    assert product.name == "Ноутбук"
    assert product.description == "Мощный"
    assert product.price == 99999.99
    assert product.quantity == 5


def test_product_price_setter_with_negative_price(capfd):
    product = Product("Телефон", "Простой", 10000, 10)
    product.price = -5000
    out, _ = capfd.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in out
    assert product.price == 10000


def test_product_price_setter_with_valid_price():
    product = Product("Телефон", "Простой", 10000, 10)
    product.price = 12000
    assert product.price == 12000


def test_product_new_product_with_invalid_type():
    data = {
        "name": "Смартфон",
        "description": "Флагман",
        "price": ["69999.99"],
        "quantity": "8"
    }
    with pytest.raises(TypeError):
        Product.new_product(data)


# === Тесты для класса Category ===
def test_category_products_property_format():
    product1 = Product("Ноутбук", "Мощный", 99999.99, 5)
    product2 = Product("Смартфон", "Флагман", 69999.99, 10)
    category = Category("Электроника", "Техника", [product1, product2])

    expected = [
        "Ноутбук, 99999 руб. Остаток: 5 шт.",
        "Смартфон, 69999 руб. Остаток: 10 шт."
    ]
    assert category.products == expected


def test_add_product_updates_counter():
    product = Product("Ноутбук", "Мощный", 99999.99, 5)
    category = Category("Электроника", "Техника")
    category.add_product(product)
    assert Category.product_count == 1
    assert product in category._products


def test_add_two_products():
    """Проверяет, что сложение двух продуктов возвращает правильную общую стоимость"""
    product1 = Product("Ноутбук", "Мощный", 100.0, 10)
    product2 = Product("Смартфон", "Флагман", 200.0, 2)

    total = product1 + product2
    assert total == 1400.0  # 100 * 10 + 200 * 2 = 1400


# def test_add_product_with_non_product():
#     """Проверяет, что при попытке сложить Product с не-Product выбрасывается TypeError"""
#     product = Product("Ноутбук", "Мощный", 100.0, 10)
#
#     with pytest.raises(TypeError):
#         product + "Не продукт"


def test_add_with_zero_quantity():
    """Проверяет, что товар с нулевым количеством не влияет на сумму"""
    product1 = Product("Ноутбук", "Мощный", 100.0, 0)
    product2 = Product("Смартфон", "Флагман", 200.0, 5)

    total = product1 + product2
    assert total == 1000.0  # 100 * 0 + 200 * 5 = 1000


def test_add_with_negative_price(capfd):
    """Проверяет, что отрицательная цена не учитывается в сумме"""
    product1 = Product("Ноутбук", "Мощный", -100.0, 10)  # сеттер заблокирует это
    product2 = Product("Смартфон", "Флагман", 200.0, 5)

    # Проверяем, что цена не установлена
    assert product1.price == 0  # так как была отрицательная цена

    total = product1 + product2
    assert total == 1000.0  # 0 * 10 + 200 * 5 = 1000


def test_product_str():
    product = Product("Ноутбук", "Мощный", 99999.99, 5)
    assert str(product) == "Ноутбук, 99999 руб. Остаток: 5 шт."


def test_category_str_with_total_quantity():
    """Проверяет, что метод __str__ возвращает общее количество товаров"""
    product1 = Product("Ноутбук", "Мощный", 99999.99, 5)
    product2 = Product("Смартфон", "Флагман", 69999.99, 10)
    category = Category("Электроника", "Техника", [product1, product2])

    assert str(category) == "Электроника, общее количество товаров: 15 шт."


def test_add_same_class_products():
    smartphone1 = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
                             "iPhone 13", 256, "Черный")
    smartphone2 = Smartphone("Samsung", "Флагман", 90000, 10, "Exynos",
                             "S23", 512, "Серебристый")
    total = smartphone1 + smartphone2
    assert total == 100000 * 5 + 90000 * 10


def test_add_different_class_products():
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
                            "iPhone 13", 256, "Черный")
    grass = LawnGrass("Трава", "Для дачи", 500, 20, "Россия",
                      "3 недели", "Зеленый")

    with pytest.raises(TypeError, match="Можно складывать только товары одного типа"):
        smartphone + grass



def test_add_products_of_different_types_raises_type_error():
    """Проверяет, что нельзя сложить товары разных типов"""
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
                            "iPhone 13", 256, "Черный")
    grass = LawnGrass("Трава", "Для дачи", 500, 20, "Россия",
                      "3 недели", "Зелёный")
    with pytest.raises(TypeError, match="Можно складывать только товары одного типа"):
        smartphone + grass


# def test_add_non_product_raises_type_error():
#     """Проверяет, что нельзя сложить товар с не-Product"""
#     smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
#                             "iPhone 13", 256, "Черный")
#     with pytest.raises(TypeError, match="Можно складывать только товары и их наследников"):
#         smartphone + 500  # Число вместо Product


# def test_add_invalid_type_to_category():
#     """Проверяет, что нельзя добавить не-Product в категорию"""
#     category = Category("Электроника", "Техника")
#     with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
#         category.add_product("Не продукт")


def test_add_subclass_to_category():
    """Проверяет, что можно добавлять наследников Product"""
    category = Category("Электроника", "Техника")
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
                            "iPhone 13", 256, "Черный")
    category.add_product(smartphone)
    assert len(category._products) == 1


def test_log_mixin_for_product(capsys):
    """Проверяет, что при создании Product выводится лог в формате Product(название, описание, цена, количество)"""
    Product("Ноутбук", "Мощный", 99999.99, 5)
    captured = capsys.readouterr()
    assert "Product(Ноутбук, Мощный, 99999.99, 5)" in captured.out


def test_log_mixin_for_smartphone(capsys):
    """Проверяет, что при создании Smartphone выводится лог в нужном формате"""
    Smartphone("iPhone", "Флагман", 100000, 5, "A15",
               "iPhone 13", 256, "Черный")
    captured = capsys.readouterr()
    assert "Smartphone(iPhone, Флагман, 100000, 5)" in captured.out


def test_log_mixin_for_lawn_grass(capsys):
    """Проверяет, что при создании LawnGrass выводится лог в нужном формате"""
    LawnGrass("Газонная трава", "Для дачи", 500, 20,
              "Россия", "3 недели", "Зелёный")
    captured = capsys.readouterr()
    assert "LawnGrass(Газонная трава, Для дачи, 500, 20)" in captured.out

def test_smartphone_initialization():
    """Проверяет инициализацию атрибутов у смартфона"""
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
                            "iPhone 13", 256, "Черный")
    assert smartphone.name == "iPhone"
    assert smartphone.description == "Флагман"
    assert smartphone.price == 100000
    assert smartphone.quantity == 5
    assert smartphone.efficiency == "A15"
    assert smartphone.model == "iPhone 13"
    assert smartphone.memory == 256
    assert smartphone.color == "Черный"


def test_smartphone_str():
    """Проверяет строковое представление смартфона"""
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15",
                            "iPhone 13", 256, "Черный")
    assert str(smartphone) == "iPhone, 100000 руб. Остаток: 5 шт., модель: iPhone 13, память: 256 ГБ, цвет: Черный"

def test_lawn_grass_initialization():
    """Проверяет инициализацию атрибутов у газонной травы"""
    grass = LawnGrass("Газонная трава", "Для дачи", 500, 20, "Россия",
                      "3 недели", "Зелёный")
    assert grass.name == "Газонная трава"
    assert grass.description == "Для дачи"
    assert grass.price == 500
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "3 недели"
    assert grass.color == "Зелёный"


def test_lawn_grass_str():
    """Проверяет строковое представление газонной травы"""
    grass = LawnGrass("Газонная трава", "Для дачи", 500, 20, "Россия",
                      "3 недели", "Зелёный")
    assert str(grass) == ("Газонная трава, 500 руб. Остаток: 20 шт., страна: Россия, "
                          "срок прорастания: 3 недели, цвет: Зелёный")


# def test_add_same_class_products():
#     """Проверяет, что товары одного класса складываются корректно"""
#     product1 = Product("Товар1", "Описание1", 100, 10)
#     product2 = Product("Товар2", "Описание2", 200, 2)
#     assert product1 + product2 == 1400  # 100 * 10 + 200 * 2


def test_add_products_of_different_types():
    """Проверяет, что нельзя сложить товары разных типов"""
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15", "iPhone 13", 256, "Черный")
    grass = LawnGrass("Газонная трава", "Для дачи", 500, 20, "Россия", "3 недели", "Зелёный")
    with pytest.raises(TypeError, match="Можно складывать только товары одного типа"):
        smartphone + grass


# def test_add_with_non_product():
#     """Проверяет, что нельзя складывать Product с не-Product"""
#     product = Product("Товар", "Описание", 100, 10)
#     with pytest.raises(TypeError, match="Можно складывать только товары и их наследников"):
#         product + "Не продукт"

def test_add_valid_product_to_category():
    """Проверяет, что можно добавить корректный продукт в категорию"""
    product = Product("Товар", "Описание", 100, 10)
    category = Category("Электроника", "Техника")
    category.add_product(product)
    assert len(category._products) == 1


# def test_add_invalid_type_to_category():
#     """Проверяет, что нельзя добавить не-Product в категорию"""
#     category = Category("Электроника", "Техника")
#     with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
#         category.add_product("Не продукт")


def test_add_smartphone_to_category():
    """Проверяет, что можно добавить смартфон в категорию"""
    smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15", "iPhone 13", 256, "Черный")
    category = Category("Электроника", "Техника")
    category.add_product(smartphone)
    assert len(category._products) == 1


def test_add_lawn_grass_to_category():
    """Проверяет, что можно добавить газонную траву в категорию"""
    grass = LawnGrass("Газонная трава", "Для дачи", 500, 20, "Россия", "3 недели", "Зелёный")
    category = Category("Сад", "Растения")
    category.add_product(grass)
    assert len(category._products) == 1

# def test_product_str():
#     """Проверяет строковое представление товара"""
#     product = Product("Товар", "Описание", 100, 10)
#     assert str(product) == "Товар, 100 руб. Остаток: 10 шт."


def test_product_add_with_zero_quantity():
    """Проверяет, что товар с нулевым количеством не влияет на сумму"""
    product1 = Product("Товар", "Описание", 100, 0)
    product2 = Product("Товар", "Описание", 200, 5)
    assert product1 + product2 == 1000  # 100 * 0 + 200 * 5 = 1000


# def test_add_with_negative_price(capfd):
#     """Проверяет, что товар с отрицательной ценой не влияет на сумму"""
#     product1 = Product("Товар", "Описание", -100, 10)  # сеттер заблокирует отрицательную цену
#     product2 = Product("Товар", "Описание", 200, 5)
#     assert product1.price == 0  # цена останется 0
#     assert product1 + product2 == 1000  # 0 * 10 + 200 * 5 = 1000
#
# def test_smartphone_str():
#     """Проверяет строковое представление смартфона"""
#     smartphone = Smartphone("iPhone", "Флагман", 100000, 5, "A15", "iPhone 13", 256, "Черный")
#     expected = "iPhone, 100000 руб. Остаток: 5 шт., модель: iPhone 13, память: 256 ГБ, цвет: Черный"
#     assert str(smartphone) == expected
#
#
# def test_lawn_grass_str():
#     """Проверяет строковое представление газонной травы"""
#     grass = LawnGrass("Газонная трава", "Для дачи", 500, 20, "Россия", "3 недели", "Зелёный")
#     expected = "Газонная трава, 500 руб. Остаток: 20 шт., страна: Россия, срок прорастания: 3 недели, цвет: Зелёный"
#     assert str(grass) == expected


def test_add_with_zero_price():
    """Проверяет, что товар с нулевой ценой не влияет на сумму"""
    product1 = Product("Товар", "Описание", 0, 10)
    product2 = Product("Товар2", "Описание2", 200, 5)
    assert product1.price == 0
    assert product1 + product2 == 1000  # 0 * 10 + 200 * 5 = 1000
