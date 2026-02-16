import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

# --- CONEXIÓN CON LA API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Gemini API Key:", type="password")

# --- INICIALIZACIÓN DEL MODELO ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Esta configuración usa el modelo más estable disponible
        model = genai.GenerativeModel(
            model_name='gemini-pro',  # Nombre estándar universal
            system_instruction=(
                "Actúa como un anciano de congregación cristiano con décadas de experiencia. "
                "Tu objetivo es dar consejos basados en la Traducción del Nuevo Mundo (2013) y jw.org. "
                "Sé empático, razonable y equilibrado. Estructura: Validación, Texto Bíblico, "
                "Referencia de la Watchtower y Sugerencia práctica."
            )
        )
    except Exception as e:
        st.error(f"Error de configuración: {e}")

# --- INTERFAZ ---
st.title("🛡️ Anciano de Bolsillo")
st.caption("Guía espiritual basada en principios bíblicos")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- PROCESAR PREGUNTA ---
if prompt := st.chat_input("¿En qué puedo ayudarte hoy, hermano?"):
    if not api_key:
        st.warning("⚠️ Por favor, ingresa la API Key en la barra lateral o en Secrets.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # MÉTODO DE GENERACIÓN SIMPLE PARA EVITAR ERRORES DE VERSIÓN
            response = model.generate_content(prompt)
            
            if response.text:
                respuesta = response.text
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
            else:
                st.error("La IA no pudo generar una respuesta. Revisa tu saldo o cuota en Google AI Studio.")
                
        except Exception as e:
            # Si 'gemini-pro' falla, el error aparecerá aquí
            st.error(f"Error técnico: {e}")
            st.info("Sugerencia: Ve a Google AI Studio y verifica que tu API Key esté activa.")
