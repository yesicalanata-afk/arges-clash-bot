import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# LEER VARIABLES DE RAILWAY
TOKEN = "8641151810:AAFcj8ICA9-w5zG9sR3dVny5g3PK--qmNNk"
CLASH_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjUwYTNiZDVkLTgwM2MtNDdkNC1iNTg2LTJkOTg3N2U3NTk4NyIsImlhdCI6MTc4MTgxOTU1Mywic3ViIjoiZGV2ZWxvcGVyL2ZlNGZkZGUwLTlk ZmUtMzVhYi0zYmE1LWI1ZmFjN2UyYmVlMCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjAuMC4wLjAiXSwidHlwZSI6ImNsaWVudCJ9XX0.ZyR4o5MRyZT9ICP9vGUTyoVxGLPhX7OUJAm2TBw8j8R41N80OGXwtNXO-cHn1N5Ys2bBT7EH1lDcJNa164RKEg"

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
