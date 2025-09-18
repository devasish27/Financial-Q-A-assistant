import pandas as pd
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA


def simple_qa(question: str, data):
    q = question.lower()
    if isinstance(data, pd.DataFrame):
        for col in data.columns:
            if col.lower() in q:
                try:
                    total = data[col].sum()
                    return f"The total value for **{col}** is {total:,}."
                except Exception:
                    return f"I found the column **{col}**, but couldn’t calculate totals."
        return None
    elif isinstance(data, str):
        keywords = ["revenue", "profit", "expense", "income", "cash"]
        for word in keywords:
            if word in q:
                for line in data.split("\n"):
                    if word in line.lower():
                        return f"Here’s what I found: *{line.strip()}*"
        return None
    else:
        return None


template = """
You are a financial assistant. Use the provided financial data to answer the user's question.

Financial Data:
{context}

Question:
{question}

Answer clearly and concisely:
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])
llm_chain = LLMChain(llm=OllamaLLM(model="llama2"), prompt=prompt)


def advanced_qa(question: str, data):
    # Case 1: PDF text → use retrieval-based QA
    if isinstance(data, str):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_text(data)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectordb = Chroma.from_texts(chunks, embedding=embeddings, persist_directory=".chroma")
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        llm = Ollama(model="llama2")
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

        try:
            answer = qa_chain.run(question)
            return answer.strip()
        except Exception as e:
            return f"⚠️ Retrieval error: {str(e)}"

    elif isinstance(data, pd.DataFrame):
        structured_answer = simple_qa(question, data)
        if structured_answer:
            return structured_answer

        try:
            context = data.head(20).to_string(index=False)  # small preview
            response = llm_chain.run({"context": context, "question": question})
            return response.strip()
        except Exception as e:
            return f"⚠️ LLM error: {str(e)}"

    else:
        return "Sorry, I couldn’t process this type of data."
