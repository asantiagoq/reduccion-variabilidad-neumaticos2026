import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# 1. CONFIGURACIÓN DE LA INTERFAZ
# =========================================================================
st.set_page_config(
    page_title="Sistema de Control de Activos - Angel Santiago",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Sistema de Optimization Operativa de Neumáticos")
st.markdown("### Programa de Innovacion Abierta — MMG Las Bambas")
st.markdown("---")

# =========================================================================
# 2. PANEL LATERAL CON FORMULARIO Y BOTÓN DE ACCIÓN
# =========================================================================
st.sidebar.markdown("# Panel de Control")
st.sidebar.write("Modifique las variables y presione Calcular para actualizar el modelo.")

# Sección de la Flota de Acarreo
with st.sidebar.form(key="panel_parametros"):
    st.header("Parámetros de la Flota")
    flota_total = st.number_input("Camiones en Inventario (CAT 797F)", min_value=1, value=60)
    disponibilidad_mecanica = st.slider("Disponibilidad Mecánica Objetivo (%)", min_value=50, max_value=100, value=83)
    horas_efectivas_dia = st.slider("Horas Efectivas de Trabajo Diario", min_value=1.0, max_value=24.0, value=21.83)
    precio_neumatico = st.number_input("Costo Unitario Neumático (USD)", min_value=1000, value=52000)

    # Sección de las Condiciones Geomecánicas por Tajo
    st.header("Condiciones por Frente de Trabajo")
    
    st.subheader("Tajo Norte")
    distancia_norte = st.number_input("Distancia a Chancadora - Norte (km)", value=4.5)
    vida_util_norte = st.number_input("Vida Útil Objetivo - Norte (horas)", value=6201)

    st.subheader("Tajo Sur")
    distancia_sur = st.number_input("Distancia a Chancadora - Sur (km)", value=3.8)
    vida_util_sur = st.number_input("Vida Útil Objetivo - Sur (horas)", value=4801)

    # Botón para procesar el formulario
    boton_calcular = st.form_submit_button(label="Calcular Parámetros Operativos")