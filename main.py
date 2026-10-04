import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. PÁGINA WEB SIMULADA PARA RENDER
app = Flask('')

@app.route('/')
def home():
    return "El bot de asesoría laboral está vivo y funcionando correctamente."

def run():
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)

# 2. CONFIGURACIÓN DE LAS LLAVES
TOKEN_TELEGRAM = os.environ.get("TOKEN_TELEGRAM")
CLAVE_GEMINI = os.environ.get("CLAVE_GEMINI")
ID_GRUPO_PERMITIDO = int(os.environ.get("ID_GRUPO_PERMITIDO", "0"))

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=CLAVE_GEMINI)

# Usamos el modelo más inteligente y actualizado
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda message: True)
def responder_grupo(message):
    # Seguridad de grupo
    if message.chat.id != ID_GRUPO_PERMITIDO:
        return

    texto_mensaje = message.text.lower()
    if bot.get_me().username.lower() in texto_mensaje or "bot" in texto_mensaje:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            # Orden directa con contexto legal estricto para España y Valencia
            prompt_contexto = (
                f"Actúa como un asesor laboral experto en España. Responde a la siguiente duda utilizando "
                f"estrictamente el Estatuto de los Trabajadores vigente y el V Convenio Colectivo de Panadería "
                f"y Pastelería de la Comunidad Valenciana. Explica la respuesta de forma clara, sencilla, "
                f"indica las condiciones exactas y cita siempre el artículo o apartado correspondiente si existe. "
                f"Pregunta del trabajador: {message.text}"
            )
            
            response = model.generate_content(prompt_contexto)
            bot.reply_to(message, response.text)
        except Exception as e:
            # Mensaje detallado por si acaso
            bot.reply_to(message, "He recibido tu pregunta, pero sigo teniendo un problema de conexión con la base de datos de Google AI Studio. Por favor, inténtalo de nuevo en unos segundos.")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()

