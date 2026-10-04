import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. CREAR UNA PÁGINA WEB FALSA PARA ENGAÑAR A RENDER
app = Flask('')

@app.route('/')
def home():
    return "El bot de asesoría laboral está vivo y funcionando correctamente."

def run():
    # Render exige que escuchemos en el puerto que ellos nos dan
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)

# CONFIGURACIÓN DE LAS LLAVES SECRETAS
TOKEN_TELEGRAM = os.environ.get("TOKEN_TELEGRAM")
CLAVE_GEMINI = os.environ.get("CLAVE_GEMINI")
ID_GRUPO_PERMITIDO = int(os.environ.get("ID_GRUPO_PERMITIDO", "0"))

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=CLAVE_GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda message: True)
def responder_grupo(message):
    if message.chat.id != ID_GRUPO_PERMITIDO:
        return

    texto_mensaje = message.text.lower()
    if bot.get_me().username.lower() in texto_mensaje or "bot" in texto_mensaje:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            response = model.generate_content(
                f"Basándote en el Estatuto y el Convenio de Pastelería de Valencia que tienes asignados, responde de forma clara a esta duda de un trabajador: {message.text}"
            )
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, "Lo siento, he tenido un problema al consultar las leyes. Inténtalo de nuevo.")

# ARRANCAR AMBAS COSAS A LA VEZ
if __name__ == "__main__":
    # Encendemos la web falsa en segundo plano
    t = Thread(target=run)
    t.start()
    # Encendemos el bot de Telegram
    bot.infinity_polling()
