import streamlit as st
import tempfile
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.readers.file.docs_reader import PDFReader
import logging

logging.basicConfig(level=logging.DEBUG)

st.title("PDF-based Q&A")

index = st.session_state.get("index")

def on_change_file():
    if "index"  in st.session_state:
        st.session_state.pop("index")

uploaded_file = st.file_uploader(label="Q&A対象のファイル", type="pdf", on_change=on_change_file)

if uploaded_file and index is None:
    with st.spinner(text="準備中..."):
        with tempfile.NamedTemporaryFile() as f:
            f.write(uploaded_file.getbuffer())

            documents = PDFReader().load_data(file=Path(f.name))

            llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)
            service_context = ServiceContext.from_defaults(llm=llm)
            index = VectorStoreIndex.from_documents(
                documents=documents,
                service_context=service_context
            )
            st.session_state["index"] = index

if index is not None:
    question = st.text_input(label="質問")
    if question:
        with st.spinner(text="検索中..."):
            query_engine = index.as_query_engine()
            answer = query_engine.query(question)
            st.write(answer.response)
            st.info(answer.source_nodes)
