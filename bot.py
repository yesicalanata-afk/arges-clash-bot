import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# LEER VARIABLES DE RAILWAY
TOKEN = "TU_TOKEN_DE_TELEGRAM_AQUÍ"
CLASH_KEY = "TU_CLASH_API_KEY_AQUÍ"

if not TOKEN or not CLASH_KEY:
    raise ValueError("ERROR: Falta TELEGRAM_TOKEN o CLASH_API_KEY en las variables de Railway.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! El bot de Arges Clash está activo y conectado correctamente. ⚔️")

def main():
    # Construir la aplicación con el token correcto
    application = Application.builder().token(TOKEN).build()
    
    # Añadir el comando /start
    application.add_handler(CommandHandler("start", start))
    
    # Arrancar el bot
    print("Bot iniciado con éxito...")
    application.run_polling()

if __name__ == '__main__':
    main()
