import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="📖")

st.title("📖 Anciano de Bolsillo")
st.caption("Investigación Bíblica Rápida")

# 1. Conexión
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos 1.5-flash porque es el que MENOS se cuelga y responde al toque
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Error: {e}")

# 2. Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat con Respuesta Instantánea
if prompt := st.chat_input("¿Qué quieres investigar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Usamos un mensaje de espera que no bloquee la pantalla
        mensaje_espera = st.empty()
        mensaje_espera.markdown("📖 *Consultando la biblioteca...*")
        
        try:
            # Le pedimos que actúe como investigador de la WOL directamente en el prompt
            instruccion = (
                f"Eres un experto en wol.jw.org. Investiga profundamente y responde de forma detallada, "
                f"citando textos bíblicos y publicaciones específicas (Atalaya, Despertad, etc.) "
                f"sobre este tema: {prompt}. Al final pon las fuentes."
            )
            
            response = model.generate_content(instruccion)
            
            mensaje_espera.empty() # Quitamos el "Consultando..."
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            mensaje_espera.empty()
            st.error(f"Se cortó la conexión: {e}")
            st.info("Probá recargar la página (F5).")
