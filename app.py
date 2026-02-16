import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

st.title("🛡️ Anciano de Bolsillo")
st.markdown("---")

# 1. Recuperar API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("No se encontró la clave GEMINI_API_KEY en los Secrets.")
    st.stop()

# 2. Configurar Google AI
try:
    genai.configure(api_key=api_key)
    
    # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
    # Intentamos usar la versión 2.5 Flash que preguntaste
    # Si quisieras la más nueva absoluta, sería 'gemini-3-flash'
    nombre_modelo = 'gemini-2.5-flash' 
    
    model = genai.GenerativeModel(
        model_name=nombre_modelo,
        system_instruction="Actúa como un anciano de congregación cristiano (Testigo de Jehová). Usa la TNM 2013 y jw.org. Sé empático, breve y bíblico."
    )
    
    # Mensaje de éxito discreto en la barra lateral
    st.sidebar.success(f"Conectado a: {nombre_modelo}")

except Exception as e:
    st.error(f"Error al configurar el modelo: {e}")

# 3. Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Intenta cambiar en el código 'gemini-2.5-flash' por 'gemini-3-flash'")
