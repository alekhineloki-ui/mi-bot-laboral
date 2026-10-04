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

# MODELO OFICIAL DE LA GENERACIÓN DE 2026
model = genai.GenerativeModel('gemini-3.5-flash-lite')

@bot.message_handler(func=lambda message: True)
def responder_grupo(message):
    if message.chat.id != ID_GRUPO_PERMITIDO:
        return

    texto_mensaje = message.text.lower()
    if bot.get_me().username.lower() in texto_mensaje or "bot" in texto_mensaje:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            # BASE DE DATOS INYECTADA DIRECTAMENTE EN EL CEREBRO DEL BOT
            prompt_contexto = (
                f"Actúa como un asesor laboral experto en España. Responde utilizando el Estatuto de los Trabajadores "
                f"y el V Convenio Colectivo de Panadería y Pastelería de la Comunidad Valenciana. "
                f"TABLAS SALARIALES OFICIALES 2026 (DOCV): "
                f"- Grupo 5: Base mensual = 1.095,55€ | Plus Convenio = 89,98€ | Anual = 17.782,95€ | Hora Art.35 = 12,69€ | Hora Art.41 = 1,83€ | Hora Art.43 = 27,64€ "
                f"- Grupo 4 (Tu Grupo): Base mensual = 1.166,56€ | Plus Convenio = 89,98€ | Anual = 18.848,10€ | Hora Art.35 = 13,47€ | Hora Art.41 = 1,97€ | Hora Art.43 = 29,34€ "
                f"- Grupo 3: Base mensual = 1.281,68€ | Plus Convenio = 89,98€ | Anual = 20.574,90€ | Hora Art.35 = 15,10€ | Hora Art.41 = 2,16€ | Hora Art.43 = 32,42€ "
                f"- Grupo 2: Base mensual = 1.399,95€ | Plus Convenio = 89,98€ | Anual = 22.348,95€ | Hora Art.35 = 16,24€ | Hora Art.41 = 2,36€ | Hora Art.43 = 35,07€ "
                f"- Grupo 1: Base mensual = 1.485,56€ | Plus Convenio = 89,98€ | Anual = 23.633,10€ | Hora Art.35 = 17,64€ | Hora Art.41 = 2,49€ | Hora Art.43 = 37,53€ "
                f"*(Nota general: El valor del Art. 42 es de 1,21€/hora para todos los grupos).* "
                f"PREVISIÓN TABLAS 2027: "
                f"El convenio establece un incremento fijo del +2,5% sobre todos los conceptos de 2026. Por ejemplo, "
                f"el Grupo 4 pasa a tener una retribución anual aproximada de 19.319,30€ brutos al año en 2027. "
                f"INSTRUCCIÓN DE RESPUESTA: Cuando te pregunten por sueldos, salarios, tablas o cuánto cobra un grupo, "
                f"extrae los datos exactos de esta lista, desglosa los conceptos en euros y explica con claridad. "
                f"Pregunta del trabajador: {message.text}"
            )
            
            response = model.generate_content(prompt_contexto)
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, f"Conexión establecida, pero Google AI Studio ha rechazado la consulta. Detalles: {str(e)[:50]}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
