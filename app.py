import streamlit as st
import pandas as pd
from modules.extractor import extract_from_pdf, extract_from_excel
from modules.qa_engine import simple_qa, advanced_qa
from modules.visualizer import show_visualizations
from modules.utils import init_session_state

st.set_page_config(
    page_title="Financial Document Q&A Assistant",
    page_icon="📊",
    layout="wide"
)

init_session_state()

st.title("📊 Financial Document Q&A Assistant")
st.markdown("Upload your **financial documents** (PDF or Excel) and explore insights interactively.")

with st.container():
    st.header("📂 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF or Excel file", type=["pdf", "xlsx", "xls"])

extracted_data = None

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    st.success(f"✅ File `{uploaded_file.name}` uploaded successfully!")

    tab1, tab2 = st.tabs(["📄 Extracted Text", "📊 Extracted Tables"])

    if file_type == "pdf":
        with tab1:
            st.info("🔎 Extracting text from PDF...")
            pdf_text = extract_from_pdf(uploaded_file)
            if pdf_text:
                st.text_area("Extracted Text (Preview)", pdf_text[:2000] + "...", height=300)
                extracted_data = pdf_text
            else:
                st.error("Failed to extract text from PDF.")

    elif file_type in ["xlsx", "xls"]:
        with tab2:
            st.info("📊 Reading Excel file...")
            df = extract_from_excel(uploaded_file)
            if isinstance(df, pd.DataFrame):
                st.dataframe(df.head(), use_container_width=True)
                extracted_data = df
                show_visualizations(df)
            else:
                st.error("Failed to read Excel file.")

if extracted_data is not None:
    st.header("💬 Ask Your Questions")

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    user_question = st.chat_input("Ask about revenue, expenses, profit...")

    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        use_llm = st.toggle("🤖 Use AI (Ollama)")

        if use_llm:
            answer = advanced_qa(user_question, extracted_data)
        else:
            answer = simple_qa(user_question, extracted_data)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)
