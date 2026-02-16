import streamlit as st
import google.generativeai as genai

st.title("🛡️ Anciano de Bolsillo")

# 1. Conexión directa
clave = st.secrets.get("GEMINI_API_KEY")

if not clave:
    st.error("No se encontró la clave en Secrets.")
else:
    try:
        genai.configure(api_key=clave)
        # Intentamos con el modelo más básico y compatible
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if prompt := st.chat_input("Escribe 'Hola' para probar:"):
            st.chat_message("user").markdown(prompt)
            
            # Instrucción simple
            response = model.generate_content(f"Responde como un anciano de congregación a esto: {prompt}")
            
            if response:
                st.chat_message("assistant").markdown(response.text)
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Si dice 'User location is not supported', es un tema de la IP del servidor de Streamlit.")
