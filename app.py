import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

# Estilos básicos
st.markdown("<style>h1{color:#2E5EAA;}</style>", unsafe_allow_html=True)

# Recuperar la clave
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el nombre de modelo más estándar y estable
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=(
                "Eres un anciano de congregación experimentado. Respondes como un pastor espiritual "
                "usando la Biblia Traducción del Nuevo Mundo (2013) y publicaciones de jw.org. "
                "Tu tono es amoroso, equilibrado y razonable. Siempre validas los sentimientos, "
                "das un texto bíblico, citas una publicación y das un consejo práctico."
            )
        )
    except Exception as e:
        st.error(f"Error de configuración: {e}")

st.title("🛡️ Anciano de Bolsillo")
st.caption("Guía espiritual leal basada en la Biblia")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de usuario
if prompt := st.chat_input("¿Qué tienes en tu corazón, hermano?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generación simplificada para evitar errores de versión
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Todavía hay un detalle técnico: {e}")
            st.info("Asegúrate de haber guardado la clave nueva en los Secrets de Streamlit.")
