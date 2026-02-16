import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

# --- ESTILOS VISUALES ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    h1 { color: #2E5EAA; }
    .stChatMessage { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Gemini API Key:", type="password")

# --- INICIALIZACIÓN DEL MODELO ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos un bloque de texto limpio para las instrucciones
        instrucciones = (
            "Eres un anciano de congregación experimentado, razonable y empático. "
            "Tu base es la Traducción del Nuevo Mundo (2013) y publicaciones de jw.org. "
            "Estructura: 1. Validación empática. 2. Texto bíblico. 3. Referencia a publicaciones. "
            "4. Consejo práctico o disciplina si es necesario. Si es un pecado grave, "
            "recomienda hablar con los ancianos locales."
        )
        model = genai.GenerativeModel(
           model_name='gemini-pro',
            system_instruction=instrucciones
        )
    except Exception as e:
        st.error(f"Error al configurar el modelo: {e}")

# --- INTERFAZ DE CHAT ---
st.title("🛡️ Anciano de Bolsillo")
st.markdown("Consejos bíblicos basados en las publicaciones del esclavo fiel.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE RESPUESTA ---
if prompt := st.chat_input("¿En qué puedo ayudarte hoy, hermano?"):
    if not api_key:
        st.warning("Por favor, configura la API Key.")
        st.stop()

    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            # Iniciamos el chat con el historial acumulado
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            
            # Guardar respuesta en el historial
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
        except Exception as e:
            st.error(f"Hubo un problema al procesar el consejo: {e}")
