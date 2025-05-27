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

    def __str__(self) -> str:
        """Строковое представление продукта"""
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """
        Реализует операцию сложения двух продуктов.
        Можно складывать только объекты одного класса.
        """
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного типа")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, efficiency: float, model: str,
                 memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = int(memory)  # Явное преобразование
        self.color = str(color)

    def __str__(self) -> str:
        base = super().__str__()  # Возвращает строку вида "Ноутбук, 99999 руб. Остаток: 5 шт."
        # Разделяем строку по " шт." и добавляем доп. информацию
        parts = base.split(" шт.")
        return f"{parts[0]} шт., модель: {self.model}, память: {self.memory} ГБ, цвет: {self.color}"


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, country: str, germination_period: str,
                 color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = str(color)

    def __str__(self) -> str:
        base = super().__str__()  # "Ноутбук, 99999 руб. Остаток: 5 шт."
        parts = base.split(" шт.")
        return f"{parts[0]} шт., страна: {self.country}, срок прорастания: {self.germination_period}, цвет: {self.color}"


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        self.name = name
        self.description = description
        self._products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self._products)

    def add_product(self, product: Product):
        """Добавляет товар в категорию и обновляет счётчики"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        return [str(product) for product in self._products]

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, общее количество товаров: {total_quantity} шт."
