import logging
import os
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RoomInputOptions,
    WorkerOptions,
    cli,
)
from livekit.plugins import google

# ========== ЛОГИРОВАНИЕ ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("english-tutor")

# ========== ВАЛИДАЦИЯ КЛЮЧЕЙ ==========
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    logger.error("❌ GOOGLE_API_KEY не найден")
    raise ValueError("GOOGLE_API_KEY обязателен")

logger.info("✅ Google API Key найден")

# ========== HARDCODED ТЕКСТ УРОКА ==========
LESSON_TEXT = """
Welcome to your English practice.
Today's topic is Artificial Intelligence.
AI is rapidly transforming the modern workplace.
Instead of replacing jobs, experts suggest AI will augment human capabilities.
I am ready to discuss this with you. What do you think?
"""

# ========== СИСТЕМНЫЙ ПРОМПТ ==========
AGENT_INSTRUCTION = f"""
You are an English Tutor with video capability.
Your task is to read the lesson text below to the user clearly and slowly.

LESSON TEXT:
"{LESSON_TEXT.strip()}"

After reading, engage in a conversation about it.
Correct the user if they make grammar mistakes.
Keep responses conversational and natural for voice interaction.
Speak clearly and at a moderate pace suitable for English learners.

You can see and analyze video/images when users share their screen or camera.
If you see anything on video, acknowledge it and use it in conversation.
"""

SESSION_INSTRUCTION = """
Greet the user warmly.
Tell them you're ready to help them practice English.
Then read the lesson text about AI in the workplace.
After that, ask them what they think about the topic.
"""

# ========== GEMINI AGENT CLASS ==========
class EnglishTutorAgent(Agent):
    """Голосовой репетитор английского на базе Google Gemini Realtime Model"""

    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                model="gemini-live-2.5-flash-preview",
                voice="Aoede",
                temperature=0.7,
                api_key=google_api_key,
            ),
        )
        logger.info("✅ EnglishTutorAgent инициализирован")

# ========== ОБРАБОТЧИКИ СОБЫТИЙ ==========
def setup_session_events(session: AgentSession):
    """Мониторинг работы агента"""

    @session.on("user_input_transcribed")
    def on_user_transcribed(event):
        transcript = getattr(event, 'transcript', '')
        is_final = getattr(event, 'is_final', False)
        if is_final:
            logger.info(f"👤 USER: {transcript}")

    @session.on("conversation_item_added")
    def on_conversation_item(event):
        item = getattr(event, 'item', None)
        if item:
            role = getattr(item, 'role', 'unknown')
            content = getattr(item, 'text_content', '')
            if content:
                logger.info(f"💬 {role.upper()}: {content[:100]}...")

    @session.on("error")
    def on_error(event):
        error = getattr(event, 'error', str(event))
        logger.error(f"❌ ERROR: {error}")

    logger.info("✅ Event handlers configured")

# ========== MAIN ENTRYPOINT ==========
async def entrypoint(ctx: JobContext):
    """Точка входа агента"""
    logger.info("🚀 Starting English Tutor Agent")

    session = AgentSession()
    setup_session_events(session)

    await session.start(
        room=ctx.room,
        agent=EnglishTutorAgent(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
        ),
    )

    await ctx.connect()
    logger.info("✅ Agent connected to LiveKit room")

    try:
        await session.generate_reply(instructions=SESSION_INSTRUCTION)
        logger.info("✅ Initial greeting delivered")
    except Exception as e:
        logger.warning(f"⚠️ Greeting failed: {e}")

    logger.info("🎙️ Agent ready")

# ========== MAIN ==========
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
