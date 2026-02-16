import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

# Estilos visuales rápidos
st.markdown("<style>h1{color:#2E5EAA;} .stChatMessage{background-color:#f0f2f6; border-radius:10px;}</style>", unsafe_allow_html=True)

st.title("🛡️ Anciano de Bolsillo")
st.caption("Consejos bíblicos para hermanos en Argentina")

# 1. Recuperar la clave de los Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Falta la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 2. Configurar el motor
try:
    genai.configure(api_key=api_key)
    # Usamos gemini-1.5-flash que es la que tus logs aceptan mejor
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al configurar Google AI: {e}")

# 3. Historial de conversación
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Entrada de usuario
if prompt := st.chat_input("¿Qué tienes en tu corazón, hermano?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción de personalidad integrada en la pregunta
            instruccion = (
                "Responde como un anciano de congregación experimentado, empático y razonable. "
                "Usa la Biblia TNM y publicaciones de jw.org. Estructura: Validación, Texto, Publicación y Consejo. "
                f"Pregunta del hermano: {prompt}"
            )
            response = st.session_state.chat.send_message(instruccion)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"El Anciano no pudo responder: {e}")
