import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Gemini API Key:", type="password")

# --- MOTOR DE LA APP ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el nombre técnico completo
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash',
            system_instruction=(
                "Eres un anciano de congregación experimentado de los Testigos de Jehová. "
                "Respondes con la Traducción del Nuevo Mundo y publicaciones de la Watchtower. "
                "Tu tono es empático, razonable y equilibrado. "
                "Estructura: Validación, Texto Bíblico, Referencia de JW.org y Sugerencia práctica."
            )
        )
    except Exception as e:
        st.error(f"Error de configuración: {e}")

st.title("🛡️ Anciano de Bolsillo")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué tienes en tu corazón?"):
    if not api_key:
        st.warning("Falta la API Key.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Respuesta directa para máxima compatibilidad
            response = model.generate_content(prompt)
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
        except Exception as e:
            # Si vuelve a dar 404, intentamos con el nombre alternativo automáticamente
            st.error(f"Error: {e}. Intenta cambiar el nombre del modelo a 'models/gemini-pro' en GitHub.")
