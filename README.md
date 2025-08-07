APITickets
API-сервис для управления тикетами пользователей. Реализованы CRUD-операции, авторизация, ролевая модель (admin/user) и логика обработки тикетов.

Стек технологий:

- [FastAPI](https://fastapi.tiangolo.com/) — backend-фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [PostgreSQL](https://www.postgresql.org/) — база данных
- [Alembic](https://alembic.sqlalchemy.org/) — миграции
- [Pytest](https://docs.pytest.org/) — тестирование
- [JWT](https://jwt.io/) — авторизация
- [Pydantic](https://docs.pydantic.dev/) — валидация данных

Структура проекта:
APITickets/
├── db_management/      # БД и SQLAlchemy модели
│   └── migration/      # Миграции
├── core/               # Создание токена
├── enums_status/       # Статусы для тикетов и пользователей
├── routers/            # FastAPI маршруты
├── schemas/            # Pydantic-схемы
├── tests/              # Тесты
├── alembic.ini
├── main.py             # Точка входа
├── pytest.ini
├── requirements.txt
├── test.db             # Тестовая база данных для тестов
└── README.md

Запуск сервера: 
uvicorn main:app --reload

Запуск тестов:
pytest

