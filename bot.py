import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración de registros (logs) para ver errores en Railway
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Comando /start en español
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usuario = update.effective_user.first_name
    mensaje_bienvenida = (
        f"¡Hola, {usuario}! 👋\n\n"
        "Bienvenido al bot oficial de **Arges Clash**.\n"
        "Pronto vas a poder consultar info de nuestro clan, guerras y jugadores.\n\n"
        "Usa /ayuda para ver los comandos disponibles."
    )
    await update.message.reply_text(mensaje_bienvenida, parse_mode="Markdown")

# Comando /ayuda en español
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje_ayuda = (
        "📌 **Comandos Disponibles:**\n\n"
        "/start - Iniciar el bot y bienvenida\n"
        "/ayuda - Mostrar este menú de ayuda\n\n"
        "⏳ _Próximamente: comandos para ver el Clan y las Guerras en vivo._"
    )
    await update.message.reply_text(mensaje_ayuda, parse_mode="Markdown")

def main() -> None:
    # Railway nos va a dar el Token de forma segura mediante esta variable
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logging.error("ERROR: No se encontró la variable TELEGRAM_TOKEN.")
        return

    # Crear la aplicación del bot
    application = Application.builder().token(TOKEN).build()

    # Registrar los comandos en español
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", ayuda))

    # Arrancar el bot
    logging.info("Arrancando el bot en modo Poll...")
    application.run_polling()

if __name__ == '__main__':
    main()
