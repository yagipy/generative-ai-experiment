import streamlit as st
import os
from datetime import datetime
from typing import Optional
import requests
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo

class GoogleCalendarAddEventArgs(BaseModel):
    event_name: str = Field(examples=["会議"])
    start_at: str = Field(examples=["2024-01-01T12:00:00+09:00"])
    end_at: str = Field(examples=["2024-01-01T12:00:00+09:00"])

@tool("google-calendar-add-event", args_schema=GoogleCalendarAddEventArgs)
def google_calendar_add_event_tool(event_name: str, start_at: str, end_at: str):
    """Google Calendar Add Event"""
    webhook_url = os.environ["MAKE_WEBHOOK_URL"]
    body = {
        "eventName": event_name,
        "startAt": start_at,
        "endAt": end_at,
    }
    result = requests.post(webhook_url, json=body)
    return f"Status: {result.status_code} - {result.text}"

@tool("clock")
def clock_tool():
    """Clock to get current datetime"""
    return datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()


st.title("Scheduling Agent")

input = st.text_input(label="何を依頼しますか？")

if input:
    with st.spinner("処理中..."):
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        tools = [
            google_calendar_add_event_tool,
            clock_tool,
        ]
        agent = create_openai_functions_agent(
            tools=tools,
            llm=llm,
            prompt=hub.pull("hwchase17/openai-functions-agent"),
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        result = agent_executor.invoke({"input": input})
        st.write(result["output"])
