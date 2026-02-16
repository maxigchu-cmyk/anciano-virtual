import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

# Recuperar la clave de los Secrets de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ No se encontró la API Key en los Secrets de Streamlit.")
    st.stop()

# Configuración simple
genai.configure(api_key=api_key)

# Definimos el modelo - Usamos 'gemini-1.5-flash' que es el estándar actual
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=(
        "Eres un anciano de congregación experimentado en Argentina. "
        "Das consejos basados en la Traducción del Nuevo Mundo (2013) y jw.org. "
        "Tu tono es empático, razonable y equilibrado. "
        "Estructura: 1. Validación, 2. Texto Bíblico, 3. Referencia de la Watchtower, 4. Sugerencia práctica."
    )
)

st.title("🛡️ Anciano de Bolsillo")
st.caption("Guía espiritual leal y equilibrada")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de usuario
if prompt := st.chat_input("¿Qué tienes en tu corazón?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generación de respuesta
            response = model.generate_content(prompt)
            texto_respuesta = response.text
            st.markdown(texto_respuesta)
            st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Prueba crear una nueva API Key en Google AI Studio.")
