from typing import Dict, Any
from typing import Optional, List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = 0  # Приватный атрибут с двойным подчеркиванием
        self.quantity = int(quantity)
        self.price = float(price)  # Вызов сеттера для проверки значения

    @property
    def price(self) -> float:
        """Геттер для получения текущей цены"""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Сеттер с проверкой: цена должна быть строго положительной"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, data: Dict[str, Any]) -> "Product":
        """
        Создаёт и возвращает новый объект класса Product на основе словаря.
        Проверяет наличие обязательных полей и типов данных.
        """
        required_fields = {
            "name": str,
            "description": str,
            "price": (int, float, str),  # Поддержка строковых чисел
            "quantity": (int, str)
        }

        for field, field_type in required_fields.items():
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

            value = data[field]

            # Проверка типа данных и автоматическое преобразование
            if not isinstance(value, field_type):
                if field == "price" or field == "quantity":
                    try:
                        if field == "quantity":
                            data[field] = int(value)
                        else:
                            data[field] = float(value)
                    except (ValueError, TypeError):
                        raise TypeError(f"Поле '{field}' должно быть числом или строкой, представляющей число")
                else:
                    raise TypeError(f"Поле '{field}' должно быть типом {field_type}")

        # Проверка на отрицательные значения только после преобразования
        if data["quantity"] < 0:
            raise ValueError("Количество товара не может быть отрицательным")
        if data["price"] < 0:
            raise ValueError("Цена товара не может быть отрицательной")

        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"]
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        self.name = name
        self.description = description
        self._products = products if products is not None else []

        # Обновляем статические счётчики
        Category.category_count += 1
        Category.product_count += len(self._products)

    def add_product(self, product: Product):
        """Добавляет товар в категорию и обновляет счётчики"""
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        """Возвращает список товаров в формате:
        'Название продукта, 80 руб. Остаток: 15 шт.'"""
        return [
            f"{product.name}, {int(product.price)} руб. Остаток: {product.quantity} шт."
            for product in self._products
        ]
