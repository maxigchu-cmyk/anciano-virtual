import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Anciano de Bolsillo - Investigador", page_icon="🛡️")

st.title("🛡️ Investigador de la Biblioteca")
st.caption("Conectado a la Biblioteca en Línea Watchtower")

# 1. Recuperar API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("No se encontró la clave GEMINI_API_KEY en los Secrets.")
    st.stop()

# 2. Configurar el Modelo con Búsqueda en Google (Grounding)
try:
    genai.configure(api_key=api_key)
    
    # Usamos las herramientas de búsqueda para que pueda "navegar" por la WOL
    # Nota: Si gemini-2.5-flash te funcionó, lo mantenemos. Si no, usa 'gemini-1.5-flash'
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash', 
        tools=[{"google_search_retrieval": {}}] # ESTO ACTIVA LA BÚSQUEDA REAL
    )
    
    # Instrucciones estrictas para la "personalidad" de búsqueda
    instrucciones_sistema = (
        "Eres un experto en investigación de la BIBLIOTECA EN LÍNEA Watchtower (wol.jw.org). "
        "Tu misión es ayudar a un hermano a encontrar información exacta. "
        "Sigue siempre estos pasos:\n"
        "1. BUSCA: Usa la herramienta de búsqueda para encontrar artículos en wol.jw.org o jw.org.\n"
        "2. INFORMACIÓN COMPLETA: Extrae la información más relevante sobre el tema.\n"
        "3. RESUMEN: Haz un resumen claro y fácil de entender.\n"
        "4. FUENTES: Al final de tu respuesta, haz una lista con las fuentes usadas "
        "(Título de la publicación, fecha, párrafo o revista).\n"
        "5. TONO: Sé siempre humilde, espiritual y animador."
    )

except Exception as e:
    st.error(f"Error de configuración: {e}")

# 3. Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué tema te gustaría investigar hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Enviamos el prompt junto con las instrucciones de búsqueda
            query_completa = f"{instrucciones_sistema}\n\nConsulta del usuario: {prompt}"
            
            # La IA decidirá si necesita buscar en internet para responder
            response = model.generate_content(query_completa)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Hubo un error en la búsqueda: {e}")
