import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de registros (logs) para ver errores en Railway
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Leer los tokens desde las variables de entorno de Railway
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CLASH_API_KEY = os.environ.get("CLASH_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {CLASH_API_KEY}",
    "Accept": "application/json"
}

def limpiar_tag(tag: str) -> str:
    """Limpia el tag quitando espacios, asegurando que empiece con # y esté en mayúsculas."""
    tag = tag.strip().upper()
    if not tag.startswith("#"):
        tag = f"#{tag}"
    return tag

def formatear_enlace(tag: str, es_jugador: bool) -> str:
    """Genera el enlace oficial de Supercell para abrir el juego directo en el perfil."""
    tag_limpio = tag.replace("#", "")
    if es_jugador:
        return f"https://link.clashofclans.com/es?action=OpenPlayerProfile&tag={tag_limpio}"
    return f"https://link.clashofclans.com/es?action=OpenClanProfile&tag={tag_limpio}"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usuario = update.effective_user.first_name
    mensaje_bienvenida = (
        f"¡Hola, {usuario}! 👋\n\n"
        "Bienvenido al bot oficial de **Arges Clash** ⚔️\n\n"
        "Enviame directamente la etiqueta (TAG) de cualquier **Jugador** o **Clan** "
        "(por ejemplo: `#9UR99R90` o `#2QCC2Y8R9`) y te daré todo su reporte con "
        "progresos, niveles y el link directo al juego.\n\n"
        "Usa /ayuda para ver más información."
    )
    await update.message.reply_text(mensaje_bienvenida, parse_mode="Markdown")

# Comando /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje_ayuda = (
        "📌 **Guía de Uso:**\n\n"
        "• No necesitas usar comandos especiales. **Solo escribe el TAG** del jugador o clan en el chat.\n"
        "• El bot detectará automáticamente si es un perfil de jugador o un clan.\n"
        "• Al final del reporte tendrás un enlace web que te abrirá el Clash of Clans directo en ese perfil.\n\n"
        "Ejemplo de TAG: `#9UR99R90`"
    )
    await update.message.reply_text(mensaje_ayuda, parse_mode="Markdown")

# Buscador inteligente de Clash of Clans
async def buscar_clash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text.strip()
    
    # Validar que al menos parezca un TAG por longitud mínima
    if len(texto) < 5:
        await update.message.reply_text("❌ Por favor, enviame un TAG válido (ejemplo: #9UR99R90).")
        return

    tag = limpiar_tag(texto)
    tag_url = tag.replace("#", "%23")
    
    # Mostrar el indicador de que el bot está escribiendo/buscando
    await update.message.reply_chat_action(action="typing")

    # 1. Intentar buscar como JUGADOR primero
    url_player = f"https://api.clashofclans.com/v1/players/{tag_url}"
    res_player = requests.get(url_player, headers=HEADERS)
    
    if res_player.status_code == 200:
        data = res_player.json()
        link = formatear_enlace(tag, es_jugador=True)
        
        reporte = (
            f"👤 **JUGADOR: {data.get('name')}** ({data.get('tag')})\n\n"
            f"🏰 **Ayuntamiento (TH):** Nivel {data.get('townHallLevel')}\n"
            f"🌟 **Nivel de Cuenta:** {data.get('expLevel')}\n"
            f"🏆 **Copas Actuales:** {data.get('trophies')} | **Máximas:** {data.get('bestTrophies')}\n"
            f"🎖️ **Estrellas en Guerra:** {data.get('warStars', 0)}\n"
            f"⚔️ **Victorias de Ataque:** {data.get('attackWins', 0)}\n"
            f"🛡️ **Defensas Ganadas:** {data.get('defenseWins', 0)}\n\n"
            f"🤝 **Tropas Donadas:** {data.get('donations', 0)}\n"
            f"📥 **Tropas Recibidas:** {data.get('donationsReceived', 0)}\n"
            f"🛡️ **Clan Actual:** {data.get('clan', {}).get('name', 'Sin Clan')}\n\n"
            f"🔗 [Abrir perfil en el Juego]({link})"
        )
        await update.message.reply_text(reporte, parse_mode="Markdown")
        return

    # 2. Si no es jugador, intentar buscar como CLAN
    url_clan = f"https://api.clashofclans.com/v1/clans/{tag_url}"
    res_clan = requests.get(url_clan, headers=HEADERS)
    
    if res_clan.status_code == 200:
        data = res_clan.json()
        link = formatear_enlace(tag, es_jugador=False)
        
        tipo_clan = "Cualquiera puede unirse" if data.get('type') == 'open' else "Invitación o Cerrado"
        
        reporte = (
            f"🏰 **CLAN: {data.get('name')}** ({data.get('tag')})\n\n"
            f"⭐ **Nivel del Clan:** {data.get('clanLevel')}\n"
            f"👥 **Miembros:** {data.get('members')}/50\n"
            f"🏆 **Puntos del Clan (Copas):** {data.get('clanPoints')}\n"
            f"🌍 **Origen:** {data.get('location', {}).get('name', 'No definido')}\n"
            f"🚪 **Acceso:** {tipo_clan}\n"
            f"🔥 **Racha de Victorias:** {data.get('warWinStreak')}\n"
            f"🏆 **Liga de Guerra (CWL):** {data.get('warLeague', {}).get('name', 'Sin Liga')}\n\n"
            f"📝 **Descripción:**\n_{data.get('description', 'Sin descripción')}_\n\n"
            f"🔗 [Abrir clan en el Juego]({link})"
        )
        await update.message.reply_text(reporte, parse_mode="Markdown")
        return

    # 3. Si no encuentra ninguno
    await update.message.reply_text(
        "❌ No encontré ningún jugador o clan con ese TAG.\n"
        "Verificá que esté bien escrito e intentalo de nuevo."
    )

def main() -> None:
    if not TOKEN or not CLASH_API_KEY:
        logging.error("ERROR: Falta TELEGRAM_TOKEN o CLASH_API_KEY en las variables de Railway.")
        return

    # Crear la aplicación del bot
    application = Application.builder().token(TOKEN).build()

    # Registrar los comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", ayuda))
    
    # Escuchar cualquier texto libre que mande el usuario (para buscar los TAGs)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_clash))

    # Arrancar el bot
    logging.info("Arrancando el bot en modo Poll con API de Clash vinculada...")
    application.run_polling()

if __name__ == '__main__':
    main()
