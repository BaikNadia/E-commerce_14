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
    assert product1 in category.products
    assert product2 in category.products


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
