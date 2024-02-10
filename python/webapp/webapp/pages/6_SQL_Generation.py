import streamlit as st
from langchain.chat_models import ChatOpenAI
from llama_index import ServiceContext, SQLDatabase
from llama_index.indices.struct_store import NLSQLTableQueryEngine
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.DEBUG)

DB_FILE = "sample.db"

st.title("SQL Generation")

question = st.text_input(label="質問")

if question:
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    service_context = ServiceContext.from_defaults(llm=llm)

    engine = create_engine(f"sqlite:///{DB_FILE}")
    sql_database = SQLDatabase(engine)
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        service_context=service_context
    )

    response = query_engine.query(question)
    st.info(response.metadata["sql_query"])
    st.info(response.metadata["result"])
    st.success(response.response)
