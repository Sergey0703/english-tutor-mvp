# Next Steps - MongoDB Integration

## ✅ Что уже сделано

1. **MongoDB Client** создан (`mongodb_client.py`) ✅
   - Подключение к MongoDB Atlas
   - Получение случайных слов
   - Поиск слов
   - Статистика словаря
   - Форматирование для урока

2. **Dependencies** добавлены ✅
   - `pymongo==4.10.1`
   - `dnspython==2.7.0`

3. **Документация** ✅
   - `MONGODB_INTEGRATION.md` - полное описание
   - `test_mongodb.py` - тестовый скрипт
   - `explore_mongodb.py` - изучение структуры

4. **Environment variables** настроены ✅
   - `.env.example` обновлён с MongoDB переменными

---

## 📋 Что нужно сделать сейчас

### Шаг 1: Тестирование локально

**Создайте файл `.env` с реальными данными:**

```bash
# LiveKit
LIVEKIT_URL=wss://first-aaelw7kf.livekit.cloud
LIVEKIT_API_KEY=APICpeSck5jt2Rm
LIVEKIT_API_SECRET=t4jZk0X3wGLvLAwh0d4iigxmrWLkrdEsmwe7FkDVYLT

# Google Gemini (НОВЫЙ ключ!)
GOOGLE_API_KEY=НОВЫЙ_КЛЮЧ_ИЗ_GOOGLE_AI_STUDIO

# MongoDB
MONGODB_URI=mongodb+srv://sergey0703:ВАШ_ПАРОЛЬ@cluster0.llssu.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=cluster0
MONGODB_COLLECTION=words
```

**Запустите тест:**

```bash
python test_mongodb.py
```

**Ожидаемый результат:**
- ✅ Connected: True
- 📊 Statistics: Total 807 words
- 🎲 Random words printed
- 📖 Untrained words printed

---

### Шаг 2: Интеграция с Agent

Нужно обновить `agent.py` чтобы использовать слова из MongoDB вместо RSS (или в комбинации).

**Два варианта:**

#### Вариант A: Только слова (без RSS)
```python
from mongodb_client import get_vocabulary_client

async def entrypoint(ctx: JobContext):
    vocab = get_vocabulary_client()

    if vocab.is_connected():
        # Получаем случайное слово
        words = vocab.get_untrained_words(count=1)
        if not words:
            words = vocab.get_random_words(count=1)

        word_data = words[0]
        lesson_text = vocab.format_word_for_lesson(word_data)
    else:
        # Fallback
        lesson_text = "Let's practice your English today..."

    # Инициализация агента с lesson_text
    ...
```

#### Вариант B: RSS + слова (комбинация)
```python
async def entrypoint(ctx: JobContext):
    vocab = get_vocabulary_client()

    # Получаем новость
    news = fetch_latest_news()
    lesson_text = format_lesson_from_news(news)

    # Добавляем слова из словаря
    if vocab.is_connected():
        words = vocab.get_random_words(count=3)
        vocab_section = "\n\nToday's vocabulary:\n"
        for word_data in words:
            word = word_data['word']
            translate = word_data['translate']
            vocab_section += f"- {word} ({translate})\n"

        lesson_text = lesson_text + vocab_section

    # Инициализация агента
    ...
```

---

### Шаг 3: Deploy на HF Spaces

После тестирования локально:

1. **Добавьте MongoDB Secrets в HF Spaces:**
   - Откройте https://huggingface.co/spaces/sergey070373/englishtutor/settings
   - Tab "Variables and secrets"
   - Добавьте 3 новых секрета:
     - `MONGODB_URI` = `mongodb+srv://sergey0703:ВАШ_ПАРОЛЬ@cluster0.llssu.mongodb.net/?retryWrites=true&w=majority`
     - `MONGODB_DB` = `cluster0`
     - `MONGODB_COLLECTION` = `words`

2. **Обновите GOOGLE_API_KEY:**
   - Создайте НОВЫЙ ключ на https://aistudio.google.com/apikey
   - Обновите секрет `GOOGLE_API_KEY` в HF Spaces

3. **Push обновлённый agent.py:**
```bash
git add agent.py
git commit -m "Integrate MongoDB vocabulary with agent"
git push hf main
```

4. **Проверьте логи:**
   - Должны увидеть: `✅ Connected to MongoDB: cluster0.words`

---

## 🎯 Roadmap интеграции

### Phase 1 (Сейчас): Базовая интеграция
- [x] MongoDB Client создан
- [x] Тестовые скрипты
- [x] Документация
- [ ] **Интеграция с agent.py** ← NEXT
- [ ] **Deploy на HF Spaces** ← NEXT
- [ ] **Тестирование через LiveKit Playground**

### Phase 2: Улучшения
- [ ] Интерактивная практика слов
- [ ] Отмечать слова как тренированные после урока
- [ ] Комбинированные уроки (RSS + vocabulary)

### Phase 3: Advanced features
- [ ] Spaced repetition algorithm
- [ ] Персонализация по уровню сложности
- [ ] Аналитика прогресса

---

## 🐛 Troubleshooting

### MongoDB не подключается локально

**Проблема:** `pymongo.errors.ServerSelectionTimeoutError`

**Решение:**
1. Проверьте MongoDB Atlas → Network Access
2. Убедитесь что `0.0.0.0/0` добавлен в IP Whitelist
3. Проверьте что connection string правильный

### HF Spaces: MongoDB connection timeout

**Решение:**
1. Убедитесь что в MongoDB Atlas → Network Access разрешен `0.0.0.0/0`
2. Проверьте что `MONGODB_URI` добавлен в Secrets (не Variables!)

### Google API Key всё ещё заблокирован

**Решение:**
1. Создайте НОВЫЙ ключ: https://aistudio.google.com/apikey
2. Удалите старый secret `GOOGLE_API_KEY` в HF Spaces
3. Добавьте новый secret с новым ключом

---

## 📞 Следующий шаг

**Давайте интегрируем MongoDB в agent.py!**

Выберите вариант:
- **A**: Только слова из словаря (без RSS)
- **B**: RSS + слова (комбинация)

Или предложите свой вариант!
