import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Anciano de Bolsillo", page_icon="🛡️")

# --- RECUPERAR API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("🔑 API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Probamos varios nombres de modelos comunes por si uno falla
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    model = None
    
    for name in model_names:
        try:
            test_model = genai.GenerativeModel(model_name=name)
            # Intento de saludo rápido para verificar si el modelo responde
            test_model.generate_content("Hola", generation_config={"max_output_tokens": 1})
            model = genai.GenerativeModel(
                model_name=name,
                system_instruction="Eres un anciano de congregación experimentado. Respondes con la Biblia TNM y publicaciones JW. Eres empático y equilibrado."
            )
            break 
        except:
            continue

    if not model:
        st.error("No se pudo conectar con ningún modelo de Gemini. Revisa si tu API Key tiene permisos en Google AI Studio.")

# --- INTERFAZ ---
st.title("🛡️ Anciano de Bolsillo")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("¿Qué tienes en tu corazón?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error al generar respuesta: {e}")
        else:
            st.warning("El motor de IA no está listo.")
