import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. PÁGINA WEB SIMULADA PARA ENGAÑAR A RENDER
app = Flask('')

@app.route('/')
def home():
    return "El bot de asesoría laboral está vivo y funcionando correctamente."

def run():
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)

# 2. CONFIGURACIÓN DE LAS LLAVES SECRETAS
TOKEN_TELEGRAM = os.environ.get("TOKEN_TELEGRAM")
CLAVE_GEMINI = os.environ.get("CLAVE_GEMINI")
ID_GRUPO_PERMITIDO = int(os.environ.get("ID_GRUPO_PERMITIDO", "0"))

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=CLAVE_GEMINI)

# Modelo hiperestable corregido sin errores tipográficos
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda message: True)
def responder_grupo(message):
    # Filtro estricto de seguridad por ID de grupo
    if message.chat.id != ID_GRUPO_PERMITIDO:
        return

    texto_mensaje = message.text.lower()
    # Reacciona si lo mencionan o si se incluye la palabra 'bot'
    if bot.get_me().username.lower() in texto_mensaje or "bot" in texto_mensaje:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            prompt_contexto = (
                f"Actúa como un asesor laboral experto en España. Responde a la siguiente duda utilizando "
                f"el Estatuto de los Trabajadores vigente y el Convenio Colectivo de Panadería y Pastelería de la "
                f"Comunidad Valenciana. Explica la respuesta de forma clara y sencilla, e indica siempre el artículo "
                f"o apartado correspondiente. Pregunta del trabajador: {message.text}"
            )
            
            response = model.generate_content(prompt_contexto)
            bot.reply_to(message, response.text)
        except Exception as e:
            # Nos avisa en el chat si hay algún otro problema con la llave de Google
            bot.reply_to(message, f"Conexión establecida, pero Google AI Studio ha rechazado la consulta. Detalles: {str(e)[:50]}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
