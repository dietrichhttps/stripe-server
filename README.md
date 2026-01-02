# Stripe Server - Django + Stripe Integration

Django сервер с интеграцией Stripe API для обработки платежей. Проект поддерживает создание платежных форм для товаров (Items) и заказов (Orders) с поддержкой скидок, налогов и множественных валют.

## Функционал

### Основные возможности:
- ✅ Django модель Item с полями (name, description, price, currency)
- ✅ API endpoint `GET /buy/{id}` - получение Stripe Session ID для оплаты Item
- ✅ API endpoint `GET /item/{id}` - HTML страница с информацией о товаре и кнопкой Buy
- ✅ Django Admin панель для управления моделями
- ✅ Поддержка переменных окружения
- ✅ Docker setup

### Бонусные возможности:
- ✅ Модель Order для объединения нескольких Items
- ✅ Модели Discount и Tax, интегрированные с Order и Stripe
- ✅ Поле Item.currency с поддержкой разных валют (USD, EUR)
- ✅ Поддержка нескольких Stripe Keypairs для разных валют
- ✅ API endpoints для Order: `GET /buy/order/{id}` и `GET /item/order/{id}`

## Установка и запуск

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd stripe-server
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Linux/Mac
# или
venv\Scripts\activate  # На Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example` и заполните его своими ключами:
```bash
cp .env.example .env
# Отредактируйте .env файл и добавьте свои Stripe ключи
```

5. Выполните миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя для доступа к админ-панели:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000

### Docker запуск

1. Создайте файл `.env` с вашими ключами (см. выше)

2. Соберите и запустите контейнер:
```bash
docker-compose up --build
```

3. Выполните миграции (в другом терминале):
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: http://localhost:8000

## Использование

### Доступ к админ-панели
- URL: http://localhost:8000/admin/
- Используйте учетные данные суперпользователя, созданные через `createsuperuser`

### API Endpoints

#### Получение Stripe Session ID для товара:
```bash
curl -X GET http://localhost:8000/buy/1
```
Ответ:
```json
{"sessionId": "cs_test_..."}
```

#### Получение HTML страницы товара:
```bash
curl -X GET http://localhost:8000/item/1
```
Ответ: HTML страница с информацией о товаре и кнопкой Buy

#### Получение Stripe Session ID для заказа:
```bash
curl -X GET http://localhost:8000/buy/order/1
```

#### Получение HTML страницы заказа:
```bash
curl -X GET http://localhost:8000/item/order/1
```

## Настройка Stripe

1. Зарегистрируйтесь на [Stripe](https://stripe.com)
2. Получите тестовые ключи в [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
3. Добавьте ключи в файл `.env`:
   - `STRIPE_PUBLISHABLE_KEY` - публичный ключ
   - `STRIPE_SECRET_KEY` - секретный ключ
   - Для поддержки разных валют добавьте соответствующие ключи (USD, EUR)

## Структура проекта

```
stripe-server/
├── store/              # Основное приложение
│   ├── models.py      # Модели: Item, Order, Discount, Tax
│   ├── views.py       # Views для API endpoints
│   ├── admin.py       # Настройки Django Admin
│   └── urls.py        # URL маршруты
├── stripe_server/     # Настройки Django проекта
│   ├── settings.py    # Настройки приложения
│   └── urls.py        # Главный URL конфиг
├── docker-compose.yml # Docker конфигурация
├── Dockerfile         # Docker образ
├── requirements.txt   # Python зависимости
└── README.md          # Документация
```

## Переменные окружения

Обязательные переменные:
- `STRIPE_SECRET_KEY` - секретный ключ Stripe
- `STRIPE_PUBLISHABLE_KEY` - публичный ключ Stripe

Опциональные переменные:
- `SECRET_KEY` - секретный ключ Django (генерируется автоматически)
- `DEBUG` - режим отладки (по умолчанию True)
- `ALLOWED_HOSTS` - разрешенные хосты (через запятую)
- `SITE_URL` - URL сайта для Stripe редиректов
- `STRIPE_SECRET_KEY_USD`, `STRIPE_SECRET_KEY_EUR` - ключи для разных валют
- `STRIPE_PUBLISHABLE_KEY_USD`, `STRIPE_PUBLISHABLE_KEY_EUR` - публичные ключи для разных валют

## Тестирование

1. Создайте товары через админ-панель (http://localhost:8000/admin/store/item/)
2. Откройте http://localhost:8000/item/1 (замените 1 на ID вашего товара)
3. Нажмите кнопку "Buy" для тестирования платежа
4. Используйте тестовые карты Stripe:
   - Успешный платеж: 4242 4242 4242 4242
   - Недостаточно средств: 4000 0000 0000 9995
   - Подробнее: https://stripe.com/docs/testing

## Лицензия

Этот проект создан в рамках тестового задания.
