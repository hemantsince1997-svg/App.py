import streamlit as st
from openai import OpenAI
import sys

# फन्ट र इन्कोडिङ मिलाउन यो जरुरी छ
sys.stdout.reconfigure(encoding='utf-8')

# १. एपको नाम र सेटिङ
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सेक्रेट्सबाट चाबी लिने
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("कृपया Secrets मा OPENAI_API_KEY हाल्नुहोस्!")
    st.stop()

# ३. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना म्यासेज देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. गफगाफ सुरु (नेपालीमा मात्र उत्तर दिने निर्देशन)
if prompt := st.chat_input("के छ खबर हेमन्त? केही सोध..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system", 
                    "content": "तपाईं हेमन्तको मिल्ने साथी हुनुहुन्छ। सधैं शुद्ध नेपाली भाषामा मात्र उत्तर दिनुहोस्। ठट्टा र रमाइलो कुरा पनि गर्नुहोस्।"
                }] + st.session_state.messages
            )
            msg = response.choices[0].message.content
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error("एआईले अहिले जवाf दिन सकेन। पछि प्रयास गर।")
