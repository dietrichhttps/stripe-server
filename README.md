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

3. Выполните миграции и соберите статические файлы (в другом терминале):
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

**Примечание:** 
- Статические файлы (CSS, JS для админ-панели) будут собраны в директорию `staticfiles/`
- Для локальной разработки рекомендуется установить `DEBUG=True` в `.env` - Django автоматически будет обслуживать статические файлы
- При `DEBUG=False` статические файлы нужно обслуживать через веб-сервер (Nginx) или использовать WhiteNoise

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
3. Добавьте ключи в файл `.env` (см. инструкцию ниже)

## Заполнение файла .env

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Откройте файл `.env` в текстовом редакторе и заполните следующие переменные:

### Минимальная конфигурация (для базовой работы)

Для начала работы достаточно заполнить основные ключи Stripe:

```env
# Django settings (можно оставить значения по умолчанию для разработки)
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SITE_URL=http://localhost:8000

# Stripe keys (обязательно!)
STRIPE_PUBLISHABLE_KEY=pk_test_ваш_публичный_ключ
STRIPE_SECRET_KEY=sk_test_ваш_секретный_ключ
```

**Где взять ключи Stripe:**
1. Войдите в [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
2. Убедитесь, что используете тестовый режим (переключатель "Test mode" вверху)
3. Скопируйте **Publishable key** (начинается с `pk_test_`) в `STRIPE_PUBLISHABLE_KEY`
4. Скопируйте **Secret key** (начинается с `sk_test_`) в `STRIPE_SECRET_KEY`
5. Если нажимаете "Reveal test key", появится секретный ключ

### Расширенная конфигурация (для поддержки разных валют)

Если вы хотите использовать разные Stripe аккаунты/ключи для разных валют (USD и EUR), заполните дополнительные поля:

```env
# Stripe keys for USD (если отличается от основных)
STRIPE_PUBLISHABLE_KEY_USD=pk_test_ваш_usd_публичный_ключ
STRIPE_SECRET_KEY_USD=sk_test_ваш_usd_секретный_ключ

# Stripe keys for EUR (если отличается от основных)
STRIPE_PUBLISHABLE_KEY_EUR=pk_test_ваш_eur_публичный_ключ
STRIPE_SECRET_KEY_EUR=sk_test_ваш_eur_секретный_ключ
```

**Примечание:** Если вы не заполните ключи для конкретной валюты (USD/EUR), будут использоваться основные ключи (`STRIPE_PUBLISHABLE_KEY` и `STRIPE_SECRET_KEY`).

### Пример заполненного .env файла

```env
# Django settings
SECRET_KEY=django-insecure-abc123xyz789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
SITE_URL=http://localhost:8000

# Stripe keys (default/fallback)
STRIPE_PUBLISHABLE_KEY=pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
STRIPE_SECRET_KEY=sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890

# Stripe keys for USD
STRIPE_PUBLISHABLE_KEY_USD=pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
STRIPE_SECRET_KEY_USD=sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890

# Stripe keys for EUR
STRIPE_PUBLISHABLE_KEY_EUR=pk_test_51XyZaBcDeFgHiJkLmNoPqRsTuVwXz9876543210
STRIPE_SECRET_KEY_EUR=sk_test_51XyZaBcDeFgHiJkLmNoPqRsTuVwXz9876543210
```

## Структура проекта

```
stripe-server/
├── store/                    # Основное приложение
│   ├── migrations/          # Миграции базы данных
│   ├── models.py            # Модели: Item, Order, Discount, Tax
│   ├── views.py             # Views для API endpoints
│   ├── admin.py             # Настройки Django Admin
│   ├── urls.py              # URL маршруты приложения
│   └── ...
├── stripe_server/           # Настройки Django проекта
│   ├── settings.py          # Настройки приложения
│   ├── urls.py              # Главный URL конфиг
│   ├── wsgi.py              # WSGI конфигурация
│   └── ...
├── .env.example             # Пример файла переменных окружения
├── .gitignore               # Git ignore правила
├── docker-compose.yml       # Docker конфигурация
├── Dockerfile               # Docker образ
├── manage.py                # Django management скрипт
├── nginx.conf               # Пример конфигурации Nginx
├── requirements.txt         # Python зависимости
└── README.md                # Документация
```

## Справочник переменных окружения

### Обязательные переменные:
- `STRIPE_SECRET_KEY` - секретный ключ Stripe (обязательно для работы платежей)
- `STRIPE_PUBLISHABLE_KEY` - публичный ключ Stripe (обязательно для работы платежей)

### Опциональные переменные:
- `SECRET_KEY` - секретный ключ Django (по умолчанию используется встроенный ключ для разработки)
- `DEBUG` - режим отладки (по умолчанию `True`, установите `False` для продакшена)
- `ALLOWED_HOSTS` - разрешенные хосты через запятую (по умолчанию `localhost,127.0.0.1`)
- `SITE_URL` - URL сайта для Stripe редиректов (по умолчанию `http://localhost:8000`)
- `STRIPE_SECRET_KEY_USD`, `STRIPE_SECRET_KEY_EUR` - секретные ключи для разных валют (если не указаны, используются основные ключи)
- `STRIPE_PUBLISHABLE_KEY_USD`, `STRIPE_PUBLISHABLE_KEY_EUR` - публичные ключи для разных валют (если не указаны, используются основные ключи)

## Тестирование

1. Создайте товары через админ-панель (http://localhost:8000/admin/store/item/)
2. Откройте http://localhost:8000/item/1 (замените 1 на ID вашего товара)
3. Нажмите кнопку "Buy" для тестирования платежа
4. Используйте тестовые карты Stripe:
   - Успешный платеж: 4242 4242 4242 4242
   - Недостаточно средств: 4000 0000 0000 9995
   - Подробнее: https://stripe.com/docs/testing

## Деплой на сервер

Проект успешно развернут и доступен онлайн:
- **URL**: https://dietrichhttps.ru
- **Админ-панель**: https://dietrichhttps.ru/admin/

Для деплоя использовались:
- VPS с Ubuntu
- Nginx как reverse proxy
- Gunicorn для запуска Django приложения
- SSL сертификат от Let's Encrypt

Подробные инструкции по деплою на сервер можно найти в истории коммитов или создать issue.

## Лицензия

Этот проект создан в рамках тестового задания.
