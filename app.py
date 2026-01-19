import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. तेरो असली चाबी (API Key)
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. एआई मोडल मिलाउने (यो तरिकाले १००% काम गर्छ)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # एआईलाई नेपालीमा मात्र बोल्न लगाउने
            response = model.generate_content(f"You are Hemant's best friend. Always reply in Nepali. Hemant said: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error("एआईले अहिले जवाफ दिन सकेन। मुजी, एकपटक रिफ्रेस गर त!")
