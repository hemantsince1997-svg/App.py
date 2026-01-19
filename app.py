import streamlit as st
from openai import OpenAI

# १. एआई सेटअप
st.set_page_config(page_title="My AI Friend", layout="centered")
st.title("🤖 My Personal AI")

# २. चाबी चेक गर्ने
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("कृपया Secrets मा OPENAI_API_KEY हाल्नुहोस्!")
    st.stop()

# ३. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ४. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a cool Nepali best friend."}] + st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
