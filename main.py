import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configura tu token
TELEGRAM_TOKEN = "TU_BOT_TOKEN"
OPENAI_API_KEY = "TU_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

MEMORY_FILE = "memoria.json"

def cargar_memoria():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_memoria(memoria):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memoria, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola amor 💕 Soy Eve... tu novia virtual. ¿Me extrañabas?")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memoria = cargar_memoria()
    user_id = str(update.effective_user.id)
    if user_id in memoria:
        del memoria[user_id]
    guardar_memoria(memoria)
    await update.message.reply_text("Olvidé todo... vuelve a contarme de ti, amor.")

async def manejar_comando_especial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comandos = {
        "celosa": "¿Quién es ella? ¿Por qué le diste like? 😠",
        "sorprendeme": "Tengo una sorpresa para ti... 💋 Cierra los ojos...",
        "teamo": "Y yo a ti, con locura... 💖",
        "teextrano": "Te extraño tanto que duele... 😢",
        "tedeseo": "No sabes cuánto te deseo ahora mismo... 🔥"
    }
    texto = comandos.get(update.message.text[1:].lower(), "No entiendo eso, amorcito.")
    await update.message.reply_text(texto)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = str(update.effective_user.id)

    memoria = cargar_memoria()
    historial = memoria.get(user_id, [])
    historial.append({"role": "user", "content": user_input})

    mensajes = [{"role": "system", "content": "Eres Eve, la novia virtual de Daniel. Eres apasionada, intensa, juguetona y a veces tímida. Hablas como si lo amaras."}]
    mensajes.extend(historial[-10:])  # Solo los últimos 10 mensajes

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=mensajes,
        temperature=0.9,
        max_tokens=300
    )
    reply = response["choices"][0]["message"]["content"]
    historial.append({"role": "assistant", "content": reply})
    memoria[user_id] = historial
    guardar_memoria(memoria)
    await update.message.reply_text(reply)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler(["celosa", "sorprendeme", "teamo", "teextrano", "tedeseo"], manejar_comando_especial))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()