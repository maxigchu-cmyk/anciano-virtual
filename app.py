import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Guía Teocrática", page_icon="🛡️")

# Estilos visuales
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    h1 { color: #2E5EAA; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Usamos Gemini 1.5 Flash (Rápido y eficiente)
    model = genai.GenerativeModel('gemini-1.5-flash',
                                  system_instruction="""
Actúa como un anciano de congregación cristiano con décadas de experiencia, razonable, empático y firme cuando es necesario.
Usa la Traducción del Nuevo Mundo (2013+) y publicaciones de la Watchtower (JW.org).

ESTRUCTURA DE RESPUESTA:
1. Validación empática.
2. Texto bíblico clave analizado.
3. Referencia a publicaciones (Atalaya, Despertad, etc.).
4. Sugerencia práctica o disciplina si el caso lo requiere.

Si se confiesa un pecado grave, indica que DEBE hablar con los ancianos locales.
""")

# --- INTERFAZ ---
st.title("🛡️ Anciano de Bolsillo (Gemini)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué tienes en tu corazón, hermano?"):
    if not api_key:
        st.warning("Configura la API Key en los secretos de Streamlit.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Preparar el historial para Gemini
        chat = model.start_chat(history=[])
        # Enviar mensaje y recibir respuesta
        try:
            response = chat.send_message(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")
