import os
import requests
import streamlit as st

# Config
API_URL_DEFAULT = "http://127.0.0.1:8000/chat/"
API_URL = os.getenv("CALASSIST_API_URL", API_URL_DEFAULT)

st.set_page_config(page_title="Calendar Assistant", page_icon="🗓️")
st.title(" Calendar Assistant")
st.caption("Escribe en lenguaje natural y yo creo/consulto eventos.")

# Barra lateral
st.sidebar.header("Ajustes")
api_url = st.sidebar.text_input("URL de tu API /chat/", API_URL)
if not api_url.endswith("/"):
    api_url += "/"

# Estado de conversación
if "history" not in st.session_state:
    st.session_state.history = []

# Mostrar historial
for role, text in st.session_state.history:
    if role == "user":
        st.chat_message("user").markdown(text)
    else:
        st.chat_message("assistant").markdown(text)

# --- Botón para limpiar chat ---
if st.sidebar.button("🧹 Limpiar chat"):
    st.session_state.history = []
    st.rerun()

# Entrada del usuario
user_msg = st.chat_input("Ej: crea una reunión con Arpa mañana a las 10")
if user_msg:
    st.session_state.history.append(("user", user_msg))
    st.chat_message("user").markdown(user_msg)

    # Llamada a tu FastAPI
    try:
        resp = requests.post(api_url, json={"question": user_msg}, timeout=25)
        if resp.ok:
            data = resp.json()
            answer = data.get("response") or str(data)
        else:
            answer = f"Error {resp.status_code}: {resp.text}"
    except Exception as e:
        answer = f" No se pudo conectar con la API: {e}"

    st.session_state.history.append(("assistant", answer))
    st.chat_message("assistant").markdown(answer)
