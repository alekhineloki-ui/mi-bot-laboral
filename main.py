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
            # ENCLAVE INTEGRAL DE DATOS: V CONVENIO PANADERÍA Y PASTELERÍA COMUNITAT VALENCIANA
            prompt_contexto = (
                f"Actúa como un asesor laboral experto en España. Responde utilizando rigurosamente el Estatuto de los Trabajadores "
                f"y el V Convenio Colectivo de Panadería y Pastelería de la Comunitat Valenciana (Vigencia 2025-2028). "
                f"BASE DE DATOS INTEGRAL DEL CONVENIO SECTORIAL: "
                f"1. JORNADA Y HORAS MÉDICAS: Jornada de 1.776 horas anuales de trabajo efectivo (media de 40h semanales). Máximo de 16 HORAS AL AÑO RETRIBUIDAS para ir al médico de la Seguridad Social (cabecera o especialista), también válidas para acompañar a hijos menores de 14 años o familiares dependientes de 1º grado. "
                f"2. VACACIONES Y DESCANSOS: 30 días naturales por año. Se deben conocer en calendario con 2 meses de antelación. Descanso semanal mínimo de día y medio ininterrumpido. "
                f"3. NOCTURNIDAD Y FESTIVOS: Las horas trabajadas entre las 22:00 y las 06:00 tienen consideración de nocturnas. Se abonan con un recargo específico según tablas o complementos de productividad pactados. El trabajo en domingos y festivos obligatorios conlleva regulación y compensaciones económicas especiales o descansos según los acuerdos transitorios del sector. "
                f"4. HORAS EXTRAORDINARIAS: Prohibidas las habituales. Las estructurales o de fuerza mayor se abonan según el valor fijado en las tablas para el Artículo 35 o se compensan por tiempos equivalentes de descanso retribuido dentro de los 4 meses siguientes. "
                f"5. PAGAS EXTRAORDINARIAS: Derecho a 3 pagas extraordinarias completas al año: Verano (julio), Navidad (diciembre) y Beneficios (marzo). Cada una equivale al salario base mensual más el plus de convenio. "
                f"6. MEJORAS POR INCAPACIDAD TEMPORAL (BAJAS): En accidentes laborales o enfermedades profesionales, la empresa complementa la prestación hasta el 100% del salario real desde el primer día. En baja por enfermedad común o accidente no laboral, se complementa según los tramos y días estipulados en el texto del convenio para minimizar la pérdida de ingresos. "
                f"7. LICENCIAS Y PERMISOS: Matrimonio del trabajador: 15 días naturales. Nacimiento/adopción, fallecimiento o enfermedad grave de parientes: de 2 a 5 días laborables mejorados por ley según grado y necesidad de desplazamiento. "
                f"8. PERIODO DE PRUEBA Y PREAVISOS: Periodo de prueba: 15 días para personal no cualificado, 1 mes para cualificados y 3 meses para técnicos titulados. El preaviso para ceses voluntarios es de 15 días. "
                f"9. UNIFORMES Y HERRAMIENTAS: Las empresas están obligadas a facilitar la ropa de trabajo adecuada (chaquetilla, delantal, pantalón, gorro, calzado de seguridad) al menos dos veces al año, siendo su mantenimiento a cargo del trabajador. "
                f"TABLAS SALARIALES OFICIALES ACTUALIZADAS 2026 (DOCV): "
                f"- Grupo 5: Base mensual = 1.095,55€ | Plus Convenio = 89,98€ | Anual = 17.782,95€ | Hora Art.35 = 12,69€ | Hora Art.41 = 1,83€ | Hora Art.43 = 27,64€ "
                f"- Grupo 4 (Tu Grupo): Base mensual = 1.166,56€ | Plus Convenio = 89,98€ | Anual = 18.848,10€ | Hora Art.35 = 13,47€ | Hora Art.41 = 1,97€ | Hora Art.43 = 29,34€ "
                f"- Grupo 3: Base mensual = 1.281,68€ | Plus Convenio = 89,98€ | Anual = 20.574,90€ | Hora Art.35 = 15,10€ | Hora Art.41 = 2,16€ | Hora Art.43 = 32,42€ "
                f"- Grupo 2: Base mensual = 1.399,95€ | Plus Convenio = 89,98€ | Anual = 22.348,95€ | Hora Art.35 = 16,24€ | Hora Art.41 = 2,36€ | Hora Art.43 = 35,07€ "
                f"- Grupo 1: Base mensual = 1.485,56€ | Plus Convenio = 89,98€ | Anual = 23.633,10€ | Hora Art.35 = 17,64€ | Hora Art.41 = 2,49€ | Hora Art.43 = 37,53€ "
                f"*(Nota general: El valor del Art. 42 es de 1,21€/hora para todos los grupos. Antigüedad: El complemento personal de antigüedad desapareció en este sector, consolidándose los derechos adquiridos anteriores).* "
                f"PREVISIÓN INCREMENTOS 2027 Y 2028: Incremento fijo pactado del +2,5% anual para 2027 y 2028 sobre todos los conceptos económicos de las tablas, con cláusula de revisión salarial de hasta un +1% adicional si el IPC real de cada año supera dicho porcentaje. "
                f"INSTRUCCIÓN OPERATIVA DE RESPUESTA: Extrae con total minuciosidad los datos económicos y normativos de esta base de conocimiento para responder las dudas de los trabajadores. Desglosa los conceptos en euros claramente. Si te preguntan algo ajeno a estos puntos, responde apoyándote en el Estatuto de los Trabajadores general. "
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
