import streamlit as st
import openai

st.title('Simple Chat Completion')

user_message = st.text_input(label="どうしましたか？")

if user_message:
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ]
    )
    st.write(completion.choices[0].message.content)
