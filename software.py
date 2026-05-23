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
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] button {
            background-color: #ff4b4b !important;
            color: white !important;
            border-radius: 5px !important;
            border: none !important;
            width: 100% !important;
            font-weight: bold !important;
            height: 3em !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #ff3333 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# =========================================================================
# 3. PROCESAMIENTO Y DESPLIEGUE DINÁMICO
# =========================================================================
if boton_calcular:
    
    # Creamos un contenedor de animación de carga para dar el efecto de recarga
    with st.spinner("Procesando telemetria y recalculando costos operativos..."):
        
        # Parámetros fijos de desgaste basados en las especificaciones
        profundidad_inicial_mm = 65.0
        neumaticos_por_camion = 6

        # Alineación de los cálculos analíticos para el Tajo Norte
        tasa_desgaste_norte = profundidad_inicial_mm / vida_util_norte
        cph_neumatico_norte = precio_neumatico / vida_util_norte
        cph_camion_norte = cph_neumatico_norte * neumaticos_por_camion

        # Alineación de los cálculos analíticos para el Tajo Sur
        tasa_desgaste_sur = profundidad_inicial_mm / vida_util_sur
        cph_neumatico_sur = precio_neumatico / vida_util_sur
        cph_camion_sur = cph_neumatico_sur * neumaticos_por_camion

        # Determinación de variaciones porcentuales del impacto operativo
        variacion_desgaste = ((tasa_desgaste_sur - tasa_desgaste_norte) / tasa_desgaste_norte) * 100
        variacion_cph = ((cph_camion_sur - cph_camion_norte) / cph_camion_norte) * 100

        # =========================================================================
        # 4. DESPLIEGUE DE INDICADORES EN PANTALLA PRINCIPAL
        # =========================================================================
        st.header("1. Cuantificación del Impacto Geomecánico y Costo por Hora")
        st.write("Resultados generados a partir de los parámetros activos en el panel de control.")

        # Distribución en columnas para presentación en paralelo
        col_nort_vista, col_sur_vista, col_var_vista = st.columns(3)
        
        with col_nort_vista:
            st.metric(
                label="CPH Camión - Tajo Norte", 
                value=f"${cph_camion_norte:.2f} USD/h", 
                delta=f"{tasa_desgaste_norte:.5f} mm/h"
            )
            
        with col_sur_vista:
            st.metric(
                label="CPH Camión - Tajo Sur", 
                value=f"${cph_camion_sur:.2f} USD/h", 
                delta=f"{tasa_desgaste_sur:.5f} mm/h",
                delta_color="inverse"
            )
            
        with col_var_vista:
            st.metric(
                label="Incremento de Costo Operativo", 
                value=f"+{variacion_cph:.1f}%", 
                delta="Severidad Geomecánica Alta",
                delta_color="off"
            )

        st.markdown("---")

        # Estructuración de la tabla consolidada para el reporte técnico
        st.subheader("Tabla Resumen de Indicadores Técnicos y Financieros")
        
        datos_resumen = {
            "Métrica Operativa": [
                "Tasa de Desgaste (mm/h)", 
                "Costo por Hora por Neumático (USD/h)", 
                "Costo por Hora por Camión (USD/h)"
            ],
            "Tajo Norte": [
                f"{tasa_desgaste_norte:.5f}", 
                f"${cph_neumatico_norte:.2f}", 
                f"${cph_camion_norte:.2f}"
            ],
            "Tajo Sur": [
                f"{tasa_desgaste_sur:.5f}", 
                f"${cph_neumatico_sur:.2f}", 
                f"${cph_camion_sur:.2f}"
            ],
            "Incremento de Impacto": [
                f"+{variacion_desgaste:.1f}%", 
                f"+{variacion_cph:.1f}%", 
                f"+{variacion_cph:.1f}%"
            ]
        }

        df_resumen = pd.DataFrame(datos_resumen)
        st.table(df_resumen)
        
    # =========================================================================
        # 5. VALIDACION DE CAPACIDAD OPERATIVA Y SANEAMIENTO (PUNTO 2 DEL PDF)
        # =========================================================================
        st.header("2. Saneamiento del Modelo de Transporte y Capacidad Operativa")
        st.write("Evaluación del cumplimiento de metas de producción bajo restricciones de disponibilidad.")

        # Parámetros técnicos de rendimiento para camiones CAT 797F
        toneladas_por_viaje = 320.0
        
        # Rendimiento estimado en viajes por hora según distancia y pendientes
        viajes_hora_norte = 1.6
        viajes_hora_sur = 1.8

        # Cálculo matemático del impacto de la disponibilidad mecánica (Restricción del taller)
        flota_disponible = (flota_total * disponibilidad_mecanica) / 100.0
        horas_flota_diarias = flota_disponible * horas_efectivas_dia

        # Asignación simulada de la flota disponible (Escenario mixto estándar 50/50)
        horas_asignadas_norte = horas_flota_diarias * 0.50
        horas_asignadas_sur = horas_flota_diarias * 0.50

        # Proyección de producción diaria real transportada (Toneladas)
        produccion_norte_ton = horas_asignadas_norte * viajes_hora_norte * toneladas_por_viaje
        produccion_sur_ton = horas_asignadas_sur * viajes_hora_sur * toneladas_por_viaje
        produccion_total_ton = produccion_norte_ton + produccion_sur_ton

        # Meta de producción estipulada para el tajo en Las Bambas (Línea base de control)
        meta_produccion_bambas = 450000.0

        # Despliegue de métricas de capacidad de transporte
        col_cap1, col_cap2, col_cap3 = st.columns(3)

        with col_cap1:
            st.metric(
                label="Flota Disponible Operativa",
                value=f"{flota_disponible:.1f} Camiones",
                delta=f"-{flota_total - flota_disponible:.1f} en Mantenimiento",
                delta_color="inverse"
            )

        with col_cap2:
            st.metric(
                label="Producción Diaria Proyectada",
                value=f"{produccion_total_ton:,.0f} Ton",
                delta=f"{produccion_total_ton - meta_produccion_bambas:,.0f} vs Meta"
            )

        with col_cap3:
            # Validación automática del cumplimiento regulatorio del PDF
            if produccion_total_ton >= meta_produccion_bambas:
                st.metric(label="Estatus de Capacidad", value="CUMPLE META", delta="Flota Saneada", delta_color="normal")
            else:
                st.metric(label="Estatus de Capacidad", value="DEFICIT OPERATIVO", delta="Requiere Optimizacion", delta_color="inverse")

        # Mensaje de diagnóstico de ingeniería
        if produccion_total_ton < meta_produccion_bambas:
            st.error(f"DIAGNOSTICO DE CAPACIDAD: Bajo una disponibilidad mecánica del {disponibilidad_mecanica}%, la flota operativa de {flota_disponible:.1f} camiones genera un déficit de {meta_produccion_bambas - produccion_total_ton:,.0f} toneladas métricas diarias respecto a la meta de producción de la mina.")
        else:
            st.success(f"DIAGNOSTICO DE CAPACIDAD: El modelo de transporte se encuentra saneado. Con el {disponibilidad_mecanica}% de disponibilidad, la capacidad instalada cubre la meta operativa diaria de {meta_produccion_bambas:,.0f} toneladas.")

    # Notificación
    st.toast("Estrategia tecnica y financiera actualizada")

else:
    # Estado inicial de la aplicación al cargar la sesión
    st.info("Por favor, configure los parámetros requeridos en la barra lateral y presione el botón 'Calcular Parámetros Operativos' para desplegar el análisis.")
