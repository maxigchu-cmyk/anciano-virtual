import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Anciano de Bolsillo 3.0", page_icon="📖")

st.title("📖 Anciano de Bolsillo")
st.caption("Impulsado por Gemini 3 Flash (2026)")

# 1. Clave API
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # LLAMADA AL MODELO 3.0 FLASH
        model = genai.GenerativeModel('gemini-3-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                # Instrucción directa en el envío para evitar latencia
                full_prompt = (
                    "Actúa como un anciano de congregación experimentado, empatico y amoroso. Ayuda, aconseja con amor. Usa la Biblia TNM de estudio y "
                    f"publicaciones de jw.org y Biblioteca en Linea para responder detalladamente a esto: {prompt}"
                )
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error de conexión con 3.0 Flash: {e}")
