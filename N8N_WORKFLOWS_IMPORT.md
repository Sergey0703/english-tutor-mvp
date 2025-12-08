# Импорт N8N Workflows на Hugging Face Spaces

## Проблема

N8N работает на порту 5678 внутри Docker контейнера, но HF Spaces пробрасывает только порт 7860.
Это значит **N8N UI недоступен извне** через браузер.

## Решение: Import через CLI

Используем N8N CLI команды для импорта workflows при старте контейнера.

---

## Вариант A: Автоматический импорт при старте (Рекомендую)

### 1. Обновить Dockerfile

Добавить копирование workflows в контейнер:

```dockerfile
# ========== COPY N8N WORKFLOWS ==========
COPY n8n_workflows/*.json /app/n8n_workflows/
```

### 2. Создать скрипт импорта

Создать файл `import_n8n_workflows.sh`:

```bash
#!/bin/bash
# Wait for N8N to start
sleep 10

# Import workflows
for workflow in /app/n8n_workflows/*.json; do
  echo "Importing workflow: $workflow"
  n8n import:workflow --input="$workflow"
done

echo "✅ All workflows imported"
```

### 3. Обновить supervisord.conf

Добавить import как третий процесс:

```ini
[program:n8n-import]
command=/bin/bash /app/import_n8n_workflows.sh
directory=/app
autostart=true
autorestart=false
startsecs=0
priority=300
```

---

## Вариант B: Manual Import через exec (если A не работает)

### 1. Подключиться к контейнеру

Если у вас есть доступ к HF Spaces terminal (через SSH или web terminal):

```bash
# Зайти в контейнер
docker exec -it <container_id> /bin/bash

# Импортировать workflows
n8n import:workflow --input=/app/n8n_workflows/rss_news_scraper.json
n8n import:workflow --input=/app/n8n_workflows/get_random_news_api.json

# Активировать workflows
n8n update:workflow --id=<workflow_id> --active=true
```

---

## Вариант C: Environment Variables (упрощенный)

Вместо N8N workflows использовать переменные окружения для хранения данных.

**Плюсы:**
- ✅ Не нужен импорт
- ✅ Данные persistent через HF Secrets

**Минусы:**
- ❌ Нельзя менять логику без rebuild
- ❌ Нет UI для редактирования

---

## Рекомендация для HF Spaces

### Сейчас (MVP):

**Использовать fallback на direct RSS** (уже реализовано в agent.py):

```python
# Agent пробует N8N, если не работает - fallback
news = fetch_news_from_n8n()
if not news:
    news = fetch_latest_news()  # Direct RSS
```

**Почему:**
- N8N workflows пусты при первом запуске
- Direct RSS работает всегда
- Нет зависимости от N8N

### Позже (Production):

**Вариант 1: N8N на Railway (отдельный сервис)**
- Полный доступ к N8N UI
- Persistent storage
- Легко настраивать workflows
- Бесплатно (free tier)

**Вариант 2: Локальный N8N + ngrok (development)**
- Полный контроль
- Быстрая разработка workflows
- Бесплатно

---

## Текущий Статус

После деплоя на HF Spaces:

1. ✅ **Agent работает** - fallback на direct RSS
2. ✅ **N8N запущен** - но workflows пусты
3. ❌ **Workflows не импортированы** - нужен Вариант A или B
4. ❌ **N8N UI недоступен** - только через exec/CLI

## Next Steps

1. **Проверить логи HF Spaces** - убедиться что N8N запустился
2. **Тестировать agent** - должен работать с fallback RSS
3. **Попробовать Вариант A** - автоматический импорт workflows
4. **Если не работает** - мигрировать N8N на Railway

---

## Альтернатива: Полностью убрать N8N из HF Spaces

**Почему:**
- Экономит ~300MB Docker image
- Убирает сложность с Supervisor
- Убирает проблему с импортом workflows
- Agent работает напрямую с RSS

**План:**
1. Удалить N8N из Dockerfile
2. Удалить Supervisor
3. Оставить только `fetch_latest_news()` в agent.py
4. Упростить до одного процесса

**Когда понадобится обработка:**
- Добавить OpenAI API в agent.py напрямую
- Или запустить N8N на Railway отдельно

---

## Решение?

**Для MVP я рекомендую:**

### Вариант SIMPLE (убрать N8N из HF Spaces):

```
[HF Spaces]
  └─ agent.py
      ├─ fetch_latest_news() - direct RSS
      └─ format_lesson_from_news() - simple formatting
```

**Плюсы:**
- ✅ Простота
- ✅ Меньший Docker image
- ✅ Меньше точек отказа
- ✅ Работает всегда

**Минусы:**
- ❌ Нет advanced обработки (keywords, translations)
- ❌ Нельзя менять логику без rebuild

---

**Что выбираем?**

1. **Оставить N8N в HF Spaces** - реализовать Вариант A (auto-import)
2. **Убрать N8N из HF Spaces** - упростить до direct RSS
3. **N8N на Railway** - перенести на отдельный сервис

Жду вашего решения после того как посмотрите результат текущего билда.
