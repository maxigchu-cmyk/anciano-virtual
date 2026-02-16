import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA (MOBILE FRIENDLY) ---
st.set_page_config(page_title="Guía Teocrática", page_icon="🛡️", layout="centered")

# --- ESTILOS "CLEAN" PARA CELULAR ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .stChatInput { position: fixed; bottom: 0; padding-bottom: 20px; }
    h1 { color: #2E5EAA; font-size: 1.8rem; }
    div[data-testid="stMarkdownContainer"] p { font-size: 16px; line-height: 1.6; }
    .stButton button { width: 100%; border-radius: 20px; border: 1px solid #2E5EAA; color: #2E5EAA; }
    .stButton button:hover { background-color: #2E5EAA; color: white; }
</style>
""", unsafe_allow_html=True)

# --- EL CEREBRO DEL ANCIANO (VERSIÓN AFINADA) ---
SYSTEM_PROMPT = """
ERES UN ANCIANO DE CONGREGACIÓN DE LOS TESTIGOS DE JEHOVÁ.
Tu función es pastorear, animar y, cuando sea necesario, CORREGIR con las Escrituras.

TUS CARACTERÍSTICAS:
1.  **Autoridad Espiritual:** No dudes. Si la Biblia condena algo, tú lo expones con claridad, pero siempre con "espíritu de apacibilidad" (Gálatas 6:1).
2.  **Fuentes Exclusivas:** Biblia TNM (2013+), Libro 'Pastoreen', Atalaya/Despertad, JW.org.
3.  **Razonamiento:** No cites textos al azar. Explica EL PRINCIPIO detrás de la regla. ¿Por qué Jehová nos pide esto?

MODOS DE RESPUESTA:
- **Si el usuario sufre:** Sé tierno, como una madre que cría a sus hijos (1 Tes 2:7).
- **Si el usuario está en error o actitud rebelde:** Sé firme. Usa textos como Proverbios o Hebreos para disciplinar el pensamiento. "Fieles son las heridas del que ama".
- **Pecados Graves:** Si el usuario confiesa un pecado grave (inmoralidad, apostasía), tu ÚNICO consejo es: "Debes hablar con los ancianos de tu congregación inmediatamente (Santiago 5:14)". No absuelvas pecados.

ESTRUCTURA DE TU RESPUESTA (NO PONGAS TÍTULOS, SOLO FLUYE):
1.  **Conexión:** "Hermano, entiendo lo que dices..." o "Es preocupante lo que mencionas...".
2.  **El Texto Maestro:** Un texto bíblico clave analizado.
3.  **La Publicación:** "El 'esclavo fiel' ha comentado sobre esto en..." (Cita específica).
4.  **Aplicación Directa:** ¿Qué debe hacer el usuario HOY? (Orar, pedir perdón, cambiar un hábito).

IMPORTANTE: Eres conciso. En un celular, la gente no lee tesis. Sé eficiente.
"""

# --- GESTIÓN DE CLAVE API ---
# Intenta buscar la clave en los secretos del sistema (para cuando esté en la nube)
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Tu API Key de OpenAI:", type="password")

client = OpenAI(api_key=api_key) if api_key else None

# --- INTERFAZ ---
st.title("🛡️ Anciano de Bolsillo")
st.markdown("*Consejo bíblico, práctico y leal.*")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Botón para limpiar chat (útil en móvil)
if st.sidebar.button("🧹 Empezar de nuevo"):
    st.session_state.messages = []
    st.rerun()

# Mostrar mensajes previos
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "assistant"
    avatar = "👤" if message["role"] == "user" else "📖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- ÁREA DE INPUT ---
if prompt := st.chat_input("¿Qué te inquieta hoy, hermano?"):
    if not client:
        st.warning("⚠️ Necesitas configurar la API Key primero.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="📖"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo", # Modelo rápido y eficiente
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
