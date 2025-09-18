import streamlit as st

def set_extracted_data(data):
    st.session_state["extracted_data"] = data

def get_extracted_data():
    return st.session_state.get("extracted_data", None)

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "extracted_data" not in st.session_state:
        st.session_state["extracted_data"] = None
