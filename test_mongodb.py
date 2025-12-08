"""
Тестовый скрипт для проверки MongoDB подключения
"""
import os
from dotenv import load_dotenv
from mongodb_client import VocabularyClient

# Загружаем переменные из .env файла
load_dotenv()

print("=" * 60)
print("Environment check:")
print(f"  MONGODB_URI: {'SET' if os.getenv('MONGODB_URI') else 'NOT SET'}")
print(f"  MONGODB_DB: {os.getenv('MONGODB_DB', 'cluster0')}")
print(f"  MONGODB_COLLECTION: {os.getenv('MONGODB_COLLECTION', 'words')}")
print("=" * 60)
print()

def test_vocabulary():
    """Тестируем все функции VocabularyClient"""

    print("=" * 60)
    print("TESTING MONGODB VOCABULARY CLIENT")
    print("=" * 60)

    # Создаём клиента
    vocab = VocabularyClient()

    # Проверяем подключение
    print(f"\nConnected: {vocab.is_connected()}")

    if not vocab.is_connected():
        print("FAILED to connect. Check MONGODB_URI")
        return

    # Статистика словаря
    print("\nVOCABULARY STATISTICS:")
    stats = vocab.get_word_count()
    print(f"  Total words: {stats['total']}")
    print(f"  Trained: {stats['trained']}")
    print(f"  Untrained: {stats['untrained']}")

    # Получаем 5 случайных слов
    print("\nRANDOM 5 WORDS:")
    random_words = vocab.get_random_words(count=5)
    for word_data in random_words:
        word = word_data.get("word")
        translate = word_data.get("translate")
        traini = word_data.get("traini", False)
        status = "[TRAINED]" if traini else "[NEW]"
        print(f"  {status} {word} - {translate}")

    # Получаем не тренированные слова
    print("\nUNTRAINED WORDS (first 3):")
    untrained = vocab.get_untrained_words(count=3)
    for word_data in untrained:
        word = word_data.get("word")
        translate = word_data.get("translate")
        print(f"  [NEW] {word} - {translate}")

    # Тестируем поиск слова
    print("\nSEARCH WORD 'epilraph':")
    word_data = vocab.search_word("epilraph")
    if word_data:
        print(f"  Found: {word_data.get('word')}")
        print(f"  Translation: {word_data.get('translate')}")
        print(f"  Transcript: {word_data.get('transcript')}")
        print(f"  Trained: {word_data.get('traini')}")

    # Форматируем слово для урока
    if word_data:
        print("\nFORMATTED FOR LESSON:")
        lesson_text = vocab.format_word_for_lesson(word_data)
        print(f"  {lesson_text}")

    # Закрываем соединение
    vocab.close()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_vocabulary()
