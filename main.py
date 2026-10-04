import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "El bot de asesoría laboral está vivo."

def run():
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)

TOKEN_TELEGRAM = os.environ.get("TOKEN_TELEGRAM")
CLAVE_GEMINI = os.environ.get("CLAVE_GEMINI")
ID_GRUPO_PERMITIDO = int(os.environ.get("ID_GRUPO_PERMITIDO", "0"))

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# CONFIGURACIÓN CORRECTA DE LA CLAVE PARA EVITAR ERRORES DE CONEXIÓN
genai.configure(api_key=CLAVE_GEMINI)

@bot.message_handler(func=lambda message: True)
def responder_grupo(message):
    if message.chat.id != ID_GRUPO_PERMITIDO:
        return

    texto_mensaje = message.text.lower()
    if bot.get_me().username.lower() in texto_mensaje or "bot" in texto_mensaje:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            # Forzamos al modelo de texto puro para que no falle en servidores gratuitos
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt_contexto = (
                f"Actúa como un asesor laboral experto en España. Responde a la siguiente duda utilizando "
                f"el Estatuto de los Trabajadores y el Convenio de Panadería y Pastelería de la Comunidad Valenciana. "
                f"Explica la respuesta de forma clara y sencilla, e indica el artículo correspondiente si existe. "
                f"Pregunta: {message.text}"
            )
            
            response = model.generate_content(prompt_contexto)
            bot.reply_to(message, response.text)
        except Exception as e:
            # Ponemos el error real en el chat para saber exactamente qué le pasa a Google
            bot.reply_to(message, f"Fallo de conexión con Google. Detalles: {str(e)[:50]}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()

