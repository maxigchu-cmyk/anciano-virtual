import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Anciano de Bolsillo", 
    page_icon="📖", 
    layout="centered"
)

# Estilo personalizado para mejorar la lectura
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    h1 { color: #4A90E2; }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 Anciano de Bolsillo")
st.subheader("Investigador de la Biblioteca en Línea")
st.info("Este asistente busca en wol.jw.org para darte respuestas bíblicas precisas.")

# --- 2. CONEXIÓN CON GEMINI ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 Error: No se encontró la API Key en los Secrets de Streamlit.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    
    # Configuramos el modelo con búsqueda en tiempo real (Google Search Grounding)
    # Esto le permite navegar por la Biblioteca en Línea
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=[{"google_search_retrieval": {}}] 
    )
    
    # Instrucciones de comportamiento
    instrucciones_sistema = (
        "Eres un anciano de congregación experto en investigación bíblica. "
        "Tu única fuente de autoridad es la Biblia (TNM 2013) y las publicaciones de los Testigos de Jehová. "
        "Cuando el usuario pregunte algo, DEBES buscar en wol.jw.org y jw.org.\n\n"
        "FORMA DE RESPONDER:\n"
        "1. Resumen detallado: Explica el tema de forma clara y amorosa.\n"
        "2. Textos bíblicos: Incluye siempre los textos clave citados en las publicaciones.\n"
        "3. Referencias exactas: Al final, haz una lista de FUENTES (ej: La Atalaya, Despertad, Libro 'Pastoreen', etc.).\n"
        "4. Tono: Siempre equilibrado, razonable y empático."
    )

except Exception as e:
    st.error(f"❌ Error al conectar con el cerebro de la IA: {e}")

# --- 3. MANEJO DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ENTRADA DE PREGUNTAS ---
if prompt := st.chat_input("¿Qué tema quieres investigar hoy?"):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    #
