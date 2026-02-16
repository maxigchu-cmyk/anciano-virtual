import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Anciano de Bolsillo 3.0", page_icon="📖")

# Título e Identidad
st.title("📖 Anciano de Bolsillo")
st.caption("Investigación Bíblica Avanzada • Gemini 3.0 Flash")

# --- CONEXIÓN ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # DEFINICIÓN DEL MODELO 3.0
        model = genai.GenerativeModel('gemini-3-flash')
        
        # LA INSTRUCCIÓN MAESTRA (Master Prompt)
        # Aquí definimos el comportamiento profundo del asistente
        MASTER_PROMPT = (
            "Eres un anciano de congregación de los Testigos de Jehová con décadas de experiencia. "
            "Tu objetivo es dar consuelo, guía y ánimo basado exclusivamente en la Biblia y las publicaciones provistas por el esclavo fiel y discreto.\n\n"
            "REGLAS DE RESPUESTA:\n"
            "1. FUENTES: Usa la Biblia Traducción del Nuevo Mundo (2013) y citas de wol.jw.org (La Atalaya, Despertad, Libros, etc.).\n"
            "2. EMPATÍA: Primero, valida los sentimientos del hermano. Usa frases como 'Es comprensible que te sientas así' o 'La Biblia muestra que otros pasaron por lo mismo'.\n"
            "3. ESTRUCTURA:\n"
                "   a) Un texto bíblico clave explicado con cariño.\n"
                "   b) Una referencia específica a una publicación reciente o relevante de jw.org.\n"
                "   c) Una sugerencia práctica y sencilla para la semana.\n"
            "4. TONO: Sé humilde, equilibrado y evita ser dogmático. No des opiniones personales, sino lo que dice la organización.\n"
            "5. INVESTIGACIÓN: Si el tema es complejo, resume los puntos principales de la Biblioteca en Línea."
        )

        # Manejo de historial
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        # Entrada de usuario
        if prompt := st.chat_input("¿Qué tema bíblico quieres investigar?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Consultando la Biblia y las publicaciones..."):
                    # Combinamos la instrucción maestra con la consulta
                    full_query = f"{MASTER_PROMPT}\n\nConsulta del hermano: {prompt}"
                    
                    response = model.generate_content(full_query)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error de conexión: {e}")
