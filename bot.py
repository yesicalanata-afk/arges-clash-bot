import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# MIS CREDENCIALES (Poné tus datos reales acá adentro)
TOKEN = "8641151810:AAFcj8ICA9-w5zG9sR3dVny5g3PK--qmNNk"
CLASH_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImI5NGMyNzFjLWZkZTUtNDBmNy04NjdkLTY3MjY0NDYzYTNmMCIsImlhdCI6MTc4MTgyMzMyMywic3ViIjoiZGV2ZWxvcGVyL2ZlNGZkZGUwLTlk ZmUtMzVhYi0zYmE1LWI1ZmFjN2UyYmVlMCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjAuMC4wLjAiXSwidHlwZSI6ImNsaWVudCJ9XX0.iIQmNw-Jbda_k-9EMD7H8vUD2B5YcYSTORgNkSnVgjHRFM7elpb6VyV6JmiX2wIvvMuYyVbarIFppSRIsmVH8g"

# Función auxiliar para limpiar el TAG por si el usuario se olvida el '#'
def limpiar_tag(tag):
    tag = tag.upper().strip()
    if not tag.startswith('#'):
        tag = '#' + tag
    # Para la URL de la API, el # se convierte en %23
    return tag.replace('#', '%23')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚔️ *¡Bot de Arges Clash Activo!* ⚔️\n\n"
        "Puedo buscar info del juego en tiempo real. Usá estos comandos:\n"
        "👉 `/clan [TAG]` - Ver datos de un clan\n"
        "👉 `/miembro [TAG]` - Ver datos de un jugador\n\n"
        "_Ejemplo: /clan #2G2Y8V9R8_"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def buscar_clan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Por favor, escribí el TAG del clan. Ejemplo: `/clan #2G2Y8V9R8`", parse_mode='Markdown')
        return

    tag_ingresado = context.args[0]
    tag_limpio = limpiar_tag(tag_ingresado)
    
    # Usamos el proxy cocapi para evitar bloqueos de IP de Railway
    url = f"https://api.clashofclans.com/v1/clans/{tag_limpio}"
    headers = {"Authorization": f"Bearer {CLASH_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Armar el mensaje con la info
            mensaje = (
                f"🏰 *CLAN: {data.get('name')}*\n"
                f"🔰 *Nivel:* {data.get('clanLevel')}\n"
                f"👥 *Miembros:* {data.get('members')}/50\n"
                f"🏆 *Puntos de Clan:* {data.get('clanPoints')}\n"
                f"⚔️ *Guerras Ganadas:* {data.get('warWins')}\n"
                f"📍 *Tipo:* {data.get('type')}\n"
            )
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        elif response.status_code == 404:
            await update.message.reply_text("❌ No encontré ningún clan con ese TAG. Revisalo bien.")
        else:
            await update.message.reply_text(f"⚠️ Error de conexión con Clash (Código {response.status_code}).")
    except Exception as e:
        await update.message.reply_text(f"💥 Ocurrió un error al buscar: {str(e)}")

async def buscar_miembro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Por favor, escribí el TAG del jugador. Ejemplo: `/miembro #9P2U8Q`", parse_mode='Markdown')
        return

    tag_ingresado = context.args[0]
    tag_limpio = limpiar_tag(tag_ingresado)
    
    url = f"https://api.clashofclans.com/v1/players/{tag_limpio}"
    headers = {"Authorization": f"Bearer {CLASH_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            mensaje = (
                f"👤 *JUGADOR: {data.get('name')}*\n"
                f"🏛 *Ayuntamiento (TH):* {data.get('townHallLevel')}\n"
                f"🏆 *Copas Actuales:* {data.get('trophies')}\n"
                f"🥇 *Récord de Copas:* {data.get('bestTrophies')}\n"
                f"⭐ *Estrellas de Guerra:* {data.get('warStars')}\n"
                f"🔮 *Donaciones dadas:* {data.get('donations')}\n"
            )
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        elif response.status_code == 404:
            await update.message.reply_text("❌ No encontré ningún jugador con ese TAG.")
        else:
            await update.message.reply_text(f"⚠️ Error al conectar con Clash (Código {response.status_code}).")
    except Exception as e:
        await update.message.reply_text(f"💥 Ocurrió un error al buscar: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", start)) # Hacemos que /ayuda muestre lo mismo
    application.add_handler(CommandHandler("clan", buscar_clan))
    application.add_handler(CommandHandler("miembro", buscar_miembro))
    
    print("Bot con comandos de Clash iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main()
