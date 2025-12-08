# N8N Workflows для English Tutor

Эта папка содержит экспортированные N8N workflows для автоматизации RSS парсинга.

## Workflows

### 1. RSS News Scraper (`rss_news_scraper.json`) ✅

**Описание:** Парсит RSS из TechCrunch, BBC, The Verge каждые 6 часов

**Nodes:**
- Schedule Trigger (every 6 hours)
- RSS Feed Read x3 (TechCrunch, BBC, The Verge)
- Merge (combine all sources)
- Filter (remove empty content)
- Format (clean HTML, limit to 500 chars)
- Save to JSON (`/app/n8n_data/processed_news.json`)

**Trigger:** Schedule (cron every 6 hours)
**Output:** JSON file с массивом новостей

---

### 2. Get Random News API (`get_random_news_api.json`) ✅

**Описание:** Webhook API для получения случайной новости

**Nodes:**
- Webhook Trigger (GET /webhook/get-news)
- Read JSON file (`processed_news.json`)
- JavaScript Code (pick random item)
- Respond to Webhook (return JSON)

**Endpoint:** `http://localhost:5678/webhook/get-news`
**Method:** GET
**Response:**
```json
{
  "title": "News title",
  "content": "First 500 chars...",
  "link": "https://...",
  "published": "2025-12-08T..."
}
```

**Error Response (no news):**
```json
{
  "error": "No news available",
  "fallback": true
}
```

## Как Импортировать

1. Открыть N8N UI: http://localhost:5678
2. Click "Import from File"
3. Выбрать `.json` файл из этой папки
4. Activate workflow

## Как Экспортировать (Backup)

1. В N8N UI открыть workflow
2. Click "..." → "Download"
3. Сохранить `.json` файл в эту папку
4. Commit в Git

## Заметки

- Файлы `.json` игнорируются Git (см. `.gitignore`)
- Это правильно, т.к. они могут содержать credentials
- Для бэкапа workflows используйте отдельный приватный репозиторий
