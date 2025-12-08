# Текущий Статус Проекта - English Tutor MVP

**Последнее обновление:** 2025-12-08 06:40 UTC
**Версия:** v0.3.0 (N8N Integration)
**Deploy Status:** 🟡 BUILDING на HF Spaces

---

## Что Работает ✅

### 1. Базовая инфраструктура
- ✅ LiveKit Cloud подключение (WebRTC voice/video)
- ✅ Google Gemini Live API integration
- ✅ Hugging Face Spaces deployment (Docker)
- ✅ GitHub integration с автоматическим деплоем
- ✅ Keep-alive через GitHub Actions (каждые 12 часов)

### 2. RSS News Integration
- ✅ Прямой парсинг RSS из TechCrunch, BBC, The Verge
- ✅ Очистка HTML контента
- ✅ Ограничение длины до 500 символов
- ✅ Fallback на hardcoded текст если RSS недоступен

### 3. Voice Agent Functionality
- ✅ Чтение новости вслух (TTS)
- ✅ Распознавание речи пользователя (STT)
- ✅ Conversation о новости с Gemini AI
- ✅ Грамматическая коррекция (встроено в Gemini)
- ✅ Video support (можно включать камеру)

---

## В Процессе 🟡

### N8N Integration (текущий билд)

**Архитектура:**
```
[HF Spaces Docker Container]
├─ Supervisor (process manager)
│  ├─ N8N (port 5678, internal only)
│  └─ LiveKit Agent (port 7860, health check)
```

**Статус:** Building на HF Spaces (ожидаем 5-10 минут)

**Что добавлено:**
- Node.js 18 installation
- N8N global install
- Supervisor для управления процессами
- 2 N8N workflows (созданы JSON, но не импортированы пока)
  - `rss_news_scraper.json` - парсинг RSS каждые 6 часов
  - `get_random_news_api.json` - webhook API для получения новости
- Agent fallback logic (пробует N8N → fallback на direct RSS)

**Ожидаемые проблемы:**
- ⚠️ Docker image size ≈ 700MB (может быть слишком большой для HF free tier)
- ⚠️ N8N UI недоступен извне (только port 7860 exposed)
- ⚠️ Workflows не импортированы автоматически
- ⚠️ Ephemeral storage (N8N data теряется при рестарте)

---

## Не Реализовано ❌

### 1. Персонализация
- ❌ База данных пользователей
- ❌ Словарь индивидуальных слов
- ❌ Прогресс обучения
- ❌ История занятий

### 2. Advanced Обработка
- ❌ Алгоритм подмены слов в тексте
- ❌ Извлечение keywords из новостей
- ❌ Переводы и объяснения
- ❌ Множественные уровни сложности

### 3. Storage & Analytics
- ❌ MongoDB integration
- ❌ Persistent хранилище для N8N workflows
- ❌ Логирование использования
- ❌ A/B тестирование методик обучения

---

## Архитектура

### Current (v0.3.0 с N8N):

```
┌─────────────────────────────────────────────────┐
│  Hugging Face Spaces (Docker)                   │
│  ┌───────────────────────────────────────────┐  │
│  │  Supervisor                               │  │
│  │  ┌────────────┐       ┌─────────────────┐ │  │
│  │  │ N8N        │       │ LiveKit Agent   │ │  │
│  │  │ (Node.js)  │◄──────│ (Python)        │ │  │
│  │  │            │ HTTP  │                 │ │  │
│  │  │ Port: 5678 │       │ Port: 7860      │ │  │
│  │  └────────────┘       └─────────────────┘ │  │
│  │       │                        │          │  │
│  │       │ RSS                    │ WebRTC   │  │
│  │       ↓                        ↓          │  │
│  │  ┌────────────┐       ┌─────────────────┐ │  │
│  │  │ TechCrunch │       │ LiveKit Cloud   │ │  │
│  │  │ BBC News   │       │ (wss://...)     │ │  │
│  │  │ The Verge  │       └─────────────────┘ │  │
│  │  └────────────┘                ↓          │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                                    ↓
                          ┌─────────────────────┐
                          │ User (Browser/Phone)│
                          └─────────────────────┘
```

### Alternative (Dockerfile.simple - fallback):

```
┌─────────────────────────────────────────────────┐
│  HF Spaces (Docker)                             │
│  ┌───────────────────────────────────────────┐  │
│  │  LiveKit Agent (Python)                   │  │
│  │  Port: 7860                               │  │
│  │                                           │  │
│  │  fetch_latest_news() → Direct RSS         │  │
│  │  format_lesson_from_news() → Clean HTML   │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

Проще, быстрее, меньший Docker image (~200MB vs ~700MB)

---

## Dependencies

### Python (requirements.txt):
```
livekit==0.17.6
livekit-agents==0.12.2
livekit-plugins-google==0.10.4
livekit-plugins-silero==0.7.5
feedparser==6.0.11
requests==2.32.3
python-dotenv==1.0.1
```

### System (Dockerfile):
```
ffmpeg, libsndfile1, supervisor, curl, gnupg
Node.js 18 (только для N8N версии)
N8N global (npm install -g n8n)
```

---

## Environment Variables

### Required (в HF Spaces Secrets):
```bash
LIVEKIT_URL=wss://first-aaelw7kf.livekit.cloud
LIVEKIT_API_KEY=APICpeSck5jt2Rm
LIVEKIT_API_SECRET=t4jZk0X3wGLvLAwh0d4iigxmrWLkrdEsmwe7FkDVYLT
GOOGLE_API_KEY=AIzaSyAl-tyw_n8fKEnBO87_BINP1EHPaUeHhrg
```

### Optional (N8N):
```bash
N8N_USER_FOLDER=/app/n8n_data
N8N_PORT=5678
N8N_HOST=0.0.0.0
N8N_BASIC_AUTH_ACTIVE=false
N8N_WEBHOOK_URL=http://localhost:5678/webhook/get-news
```

---

## Git Repositories

### GitHub (Primary):
- URL: https://github.com/Sergey0703/english-tutor-mvp
- Remote name: `github`
- Auto-deploy: ❌ (manual push)

### Hugging Face Spaces:
- URL: https://huggingface.co/spaces/sergey070373/english-tutor-mvp
- Remote name: `hf`
- Auto-deploy: ✅ (на каждый push)
- Status: https://huggingface.co/spaces/sergey070373/english-tutor-mvp

**Push command:**
```bash
git push github main && git push hf main
```

---

## Recent Commits

```
cf157c4 - Add N8N workflows documentation and simplified Dockerfile
9ef6ae0 - Add N8N integration to HF Spaces Docker container
1983c9f - Fix HF Spaces health check: configure LiveKit HTTP server on port 7860
62b7291 - Add RSS news integration for dynamic lesson content
fc30b96 - Simplify agent: remove HTTP health server, add GitHub Actions keep-alive
```

---

## Testing URLs

### LiveKit Playground:
- URL: https://agents-playground.livekit.io
- Connect with LiveKit credentials (см. Environment Variables)

### HF Space Health Check:
```bash
curl -I https://sergey0703-english-tutor-mvp.hf.space
```

---

## Known Issues

### Issue #1: N8N UI Inaccessibility
- **Problem:** Port 5678 не exposed, N8N UI нельзя открыть в браузере
- **Workaround:** Создавать workflows локально, импортировать через CLI
- **Status:** 🟡 Workaround exists

### Issue #2: Ephemeral Storage
- **Problem:** HF Spaces ephemeral storage → N8N data теряется при рестарте
- **Workaround:** Store workflows в Git, re-import при старте
- **Status:** 🟡 Workaround exists

### Issue #3: Docker Image Size
- **Problem:** Python + Node.js + N8N ≈ 700MB, может превысить лимиты
- **Workaround:** Use Dockerfile.simple (без N8N)
- **Status:** ⏳ Waiting for build result

### Issue #4: Keep-Alive Reliability
- **Problem:** GitHub Actions может не предотвратить sleep через 48 часов
- **Workaround:** UptimeRobot (внешний мониторинг) или платный HF tier
- **Status:** 🟡 Monitoring in progress

---

## Next Steps

### Immediate (после завершения билда):
1. ✅ Проверить логи HF Spaces
2. ✅ Тестировать через LiveKit Playground
3. ✅ Принять решение о N8N:
   - Если билд успешен → импортировать workflows
   - Если failed → switch на Dockerfile.simple

### Short-term (1-2 дня):
1. Решить проблему N8N workflows import
2. Добавить больше RSS источников
3. Улучшить форматирование текста новостей
4. Добавить basic logging (JSON file или console)

### Medium-term (1 неделя):
1. N8N на Railway (отдельный сервис) или убрать совсем
2. MongoDB integration для хранения словаря
3. Алгоритм подмены слов в тексте
4. Multi-user support

### Long-term (1 месяц+):
1. Персонализация по уровню пользователя
2. Аналитика прогресса обучения
3. Мобильное приложение (React Native + LiveKit SDK)
4. Интеграция с Anki для spaced repetition

---

## Documentation Files

- `README.md` - Project overview
- `CLAUDE.md` - Project instructions для Claude AI
- `N8N_HF_SPACES_SETUP.md` - N8N в HF Spaces (ограничения)
- `N8N_WORKFLOWS_IMPORT.md` - Как импортировать workflows
- `POST_DEPLOY_CHECKLIST.md` - Что делать после деплоя
- `STATUS.md` - Этот файл (текущий статус)
- `n8n_workflows/README.md` - Описание workflows
- `Dockerfile` - Текущий (с N8N)
- `Dockerfile.simple` - Fallback (без N8N)
- `supervisord.conf` - Process manager config
- `agent.py` - Main agent code

---

## Monitoring & Logs

### GitHub Actions:
- Workflow: "Keep HF Space Awake"
- Schedule: Every 12 hours (cron: `0 */12 * * *`)
- URL: https://github.com/Sergey0703/english-tutor-mvp/actions

### HF Spaces Logs:
- URL: https://huggingface.co/spaces/sergey070373/english-tutor-mvp
- Tab: "Logs"
- Real-time: да

---

**Статус на 2025-12-08 06:40:**

🟡 **BUILDING** - Ждем результата билда с N8N integration (5-10 минут)

После завершения билда → см. `POST_DEPLOY_CHECKLIST.md`
