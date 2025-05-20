import pytest

from src.classes import Category, Product


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


def test_add_product_with_non_product():
    """Проверяет, что при попытке сложить Product с не-Product выбрасывается TypeError"""
    product = Product("Ноутбук", "Мощный", 100.0, 10)

    with pytest.raises(TypeError):
        product + "Не продукт"


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


def test_category_str():
    category = Category("Электроника", "Техника", [])
    assert str(category) == "Электроника, количество продуктов: 0 шт."
