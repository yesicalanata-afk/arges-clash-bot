import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURACIÓN ---
TOKEN = "8641151810:AAFcj8ICA9-w5zG9sR3dVny5g3PK--qmNNk"
CLASH_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImI5NGMyNzFjLWZkZTUtNDBmNy04NjdkLTY3MjY0NDYzYTNmMCIsImlhdCI6MTc4MTgyMzMyMywic3ViIjoiZGV2ZWxvcGVyL2ZlNGZkZGUwLTlk ZmUtMzVhYi0zYmE1LWI1ZmFjN2UyYmVlMCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjAuMC4wLjAiXSwidHlwZSI6ImNsaWVudCJ9XX0.iIQmNw-Jbda_k-9EMD7H8vUD2B5YcYSTORgNkSnVgjHRFM7elpb6VyV6JmiX2wIvvMuYyVbarIFppSRIsmVH8g" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def limpiar_tag(tag):
    return tag.replace('#', '').upper()

async def buscar_clan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Escribí el TAG del clan.")
        return
    tag = limpiar_tag(context.args[0])
    url = f"https://api.clashofclans.com/v1/clans/%23{tag}"
    headers = {"Authorization": f"Bearer {CLASH_KEY}"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            await update.message.reply_text(f"⚔️ Clan: {data.get('name')}\n🛡️ Nivel: {data.get('clanLevel')}")
        else:
            await update.message.reply_text(f"Error {res.status_code}: Verificá tu clave.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def buscar_miembro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Escribí el TAG del jugador.")
        return
    tag = limpiar_tag(context.args[0])
    url = f"https://api.clashofclans.com/v1/players/%23{tag}"
    headers = {"Authorization": f"Bearer {CLASH_KEY}"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            await update.message.reply_text(f"👤 Jugador: {data.get('name')}\n🏆 Copas: {data.get('trophies')}")
        else:
            await update.message.reply_text(f"Error {res.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("clan", buscar_clan))
    app.add_handler(CommandHandler("jugador", buscar_miembro))
    app.run_polling()
