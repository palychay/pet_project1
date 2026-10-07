# AI Bridge — Gemini клиент

Небольшое веб-приложение: фронтенд на чистом HTML/JS отправляет промпт во FastAPI-бэкенд, тот обращается к Gemini API, сохраняет запрос и ответ в SQLite и показывает историю запросов по IP-адресу пользователя.

```
Frontend (index.html) → FastAPI (main.py) → Gemini API
                                ↓
                         SQLite (requests.db)
```

## Возможности

- Отправка промптов в Gemini и получение ответа в браузере
- История запросов, привязанная к IP-адресу
- Индикатор доступности API
- Отправка по `Ctrl/⌘ + Enter`

## Стек

- **Backend:** Python, FastAPI, Uvicorn
- **БД:** SQLite + SQLAlchemy 2.x
- **AI:** Google Gemini (`google-genai`)
- **Frontend:** HTML, CSS, vanilla JS

## Структура проекта

```
.
├── main.py           # FastAPI-приложение, эндпоинты, CORS
├── ai_client.py      # клиент Gemini
├── db.py             # модель ChatRequests и работа с БД
├── config.py         # чтение API-ключа из key.txt
├── index.html        # фронтенд
├── requirements.txt
└── key.txt           # API-ключ Gemini (создаётся вручную, не коммитить!)
```

## Установка и запуск

### 1. Клонирование и окружение

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd <ПАПКА_ПРОЕКТА>

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API-ключ

Получите ключ в [Google AI Studio](https://aistudio.google.com/) и сохраните его в файл `key.txt` в корне проекта (только ключ, без кавычек):

```
YOUR_GEMINI_API_KEY
```

> ⚠️ Добавьте `key.txt` и `requests.db` в `.gitignore`, чтобы не опубликовать ключ и историю запросов.

### 3. Запуск бэкенда

```bash
uvicorn main:app --reload --port 8000
```

API будет доступен на `http://localhost:8000`, документация Swagger — на `http://localhost:8000/docs`.
Таблицы в `requests.db` создаются автоматически при старте.

### 4. Запуск фронтенда

Фронтенд должен работать на порту **5500** или **5501** (они разрешены в CORS):

```bash
python -m http.server 5500
```

Откройте `http://localhost:5500` (или используйте расширение Live Server в VS Code).

## API

| Метод | Путь        | Описание                                   |
|-------|-------------|--------------------------------------------|
| GET   | `/requests` | История запросов текущего IP               |
| POST  | `/requests` | Отправить промпт, получить ответ от Gemini |

**Пример POST-запроса:**

```bash
curl -X POST http://localhost:8000/requests \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Привет! Расскажи о FastAPI в двух предложениях."}'
```

**Ответ:**

```json
{ "answer": "..." }
```

## Конфигурация

- **Модель Gemini** меняется в `ai_client.py`
- **Разрешённые origin'ы** для CORS — в `main.py` (`allow_origins`)
- **Адрес API** для фронтенда — константа `API_URL` в `index.html`
- **Файл БД** — `requests.db` (путь задаётся в `db.py`)
