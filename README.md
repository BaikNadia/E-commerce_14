# Проект E-commerce_14 
реализует загрузку данных о категориях товаров и продуктах из JSON-файла 
(data/products.json) и создает объекты классов Product и Category для дальнейшей работы.

## Функционал:
Чтение данных из JSON-файла.
Создание объектов класса Product (товары) и Category (категории).
Автоматический подсчёт количества категорий и товаров.

## Структура проекта:
E-commerce_14/
├── data/  
│   └── products.json       # Файл с данными  
├── src/  
│   ├── classes.py          # Классы Product и Category  
│   └── utils.py            # Функция загрузки данных из JSON  
├── tests/  
│   └── test_classes.py     # Тесты для классов  
├── main.py                 # Основной скрипт  
└── README.md               # Документация  

## Установка и запуск:
Клонируйте репозиторий.
Установите зависимости (если используется Poetry)
Убедитесь, что файл data/products.json существует
Запустите проект: python main.py




