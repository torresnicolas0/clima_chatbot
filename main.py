# main.py

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from model.chatbot import WeatherChatbot
from dotenv import load_dotenv
from log_config import get_logger

logger = get_logger(__name__)

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

weather_bot = WeatherChatbot()

async def start_command(update: Update, context: CallbackContext) -> None:
    """Envía un mensaje cuando se emite el comando /start."""
    user = update.effective_user
    welcome_message = f"Hola {user.mention_html()}! Hazme una pregunta sobre el clima de algún lugar. Si tienes dudas, puedes usar el comando /ayuda."
    await update.message.reply_html(welcome_message)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Envía un mensaje cuando se emite el comando /ayuda."""
    help_text = ("Puedes hacer preguntas sobre el clima actual en la ciudad que desees.\n"
                 "También puedes hacer más de una pregunta o incluir varias ciudades en la misma pregunta.\n"
                 "Estos son los temas de los que podré responder según mi entrenamiento: 'Tiempo actual', "
                 "'Clima actual', 'Día y noche', 'Luna y estación', 'Geolocalización'.")
    await update.message.reply_text(help_text)

async def process_message(update: Update, context: CallbackContext) -> None:
    """Procesa y responde a mensajes generales."""
    try:
        response_message = weather_bot.process_query(update.message.text)
        await update.message.reply_text(response_message)
    except Exception as e:
        logger.error(f"Error al procesar la consulta: {e}")
        await update.message.reply_text("Lo siento, ocurrió un error al procesar tu mensaje.")

def main() -> None:
    """Inicia el bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
