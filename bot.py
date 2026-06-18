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
        await update.message.reply_text("❌ Escribí el TAG del clan.")
        return
    tag_limpio = limpiar_tag(context.args[0])
    url = f"https://api.clashofclans.com/v1/clans/{tag_limpio}"
    try:
        # Usamos tu clave tal como la tienes definida
        headers = {"Authorization": f"Bearer {CLASH_KEY}"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            msg = f"⚔️ Clan: {data.get('name')}\n🛡️ Nivel: {data.get('clanLevel')}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"⚠️ Error {response.status_code}: Asegura que la IP 0.0.0.0 esté en tu clave oficial.")
    except Exception as e:
        await update.message.reply_text(f"🚨 Error: {str(e)}")

async def buscar_miembro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Escribí el TAG del jugador.")
        return
    tag_limpio = limpiar_tag(context.args[0])
    url = f"https://api.clashofclans.com/v1/players/{tag_limpio}"
    try:
        headers = {"Authorization": f"Bearer {CLASH_KEY}"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            msg = f"👤 Jugador: {data.get('name')}\n🏆 Copas: {data.get('trophies')}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"⚠️ Error {response.status_code}: Revisa tu clave en developer.clashofclans.com")
    async def buscar_miembro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Por favor, escribí el TAG del jugador.")
        return

    tag_limpio = limpiar_tag(context.args[0])
    url = f"https://api.clashofclans.com/v1/players/{tag_limpio}"

    try:
        headers = {"Authorization": f"Bearer {CLASH_KEY}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            msg = f"👤 *JUGADOR:* {data.get('name')}\n🏆 *Copas:* {data.get('trophies')}"
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"⚠️ Error {response.status_code}: No se encontró el jugador.")
    except Exception as e:
        await update.message.reply_text(f"🚨 Error de conexión: {str(e)}")

    tag_limpio = limpiar_tag(context.args[0])
    url = f"https://api.clashofclans.com/v1/players/{tag_limpio}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            msg = f"👤 *JUGADOR:* {data.get('name')}\n🏆 *Copas:* {data.get('trophies')}"
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"⚠️ Error {response.status_code}: No se encontró el jugador.")
    except Exception as e:
        await update.message.reply_text(f"🚨 Error de conexión: {str(e)}")
        
    
    print("Bot con comandos de Clash iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main()
