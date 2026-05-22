# Optimización Técnica y Financiera de Neumáticos Mineros | Innovadores en Acción
Esta es una plataforma analítica interactiva desarrollada en Python para mitigar la variabilidad en el consumo de neumáticos en la flota de acarreo CAT 797F de tajo abierto.

##  Contexto del Proyecto
En las operaciones mineras de tajo abierto, los neumáticos representan entre el 20% y el 30% del costo total de mantenimiento de la flota de acarreo. Este proyecto presenta una solución vista desde el lado de la Ingeniería de Sistemas y la Analítica Predictiva de Datos para modelar y optimizar la gestión de neumáticos bajo condiciones geomecánicas opuestas entre frentes de trabajo (Tajo Norte vs. Tajo Sur).

##  Alcance de la Solución
El sistema se estructura en dos fases de madurez tecnológica:
1. **Fase 1 (Enfoque Preventivo):** Cuantificación del impacto geomecánico (Costo por Hora - CPH), validación de la capacidad de transporte de la flota (Disponibilidad Mecánica al 83%) y control predictivo de límites térmicos (TKPH).
2. **Fase 2 (Enfoque Predictivo):** Simulación de arquitectura de Machine Learning basada en telemetría y sensores IoT para romper la dependencia de promedios estáticos y estabilizar la incertidumbre presupuestaria.

##  Tecnologías Utilizadas
* **Lenguaje:** Python 3.14.0
* **Framework Web:** Streamlit
* **Análisis de Datos:** Pandas y NumPy

##  Instrucciones para Ejecución Local
1. Clonar el repositorio:
git clone https://github.com/asantiagoq/reduccion-variabilidad-neumaticos2026

2. Instalar las dependencias requeridas:
pip install -r requirements.txt

3. Ejecutar la aplicación web:
streamlit run software.py