import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="हेमन्तको AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Non-Stop)")

# यो कोठामा भर्खरै पठाएको नयाँ चाबी हाल मुजी!
API_KEY = "AIzaSyBiEJMy2ZeTqilGIUQ4k54Q2vpSCONxQ9s"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"You are Hemant's best friend. Talk in Nepali. Hemant says: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except:
            st.error("गुगलले अझै टेरेन, १ घण्टा मोबाइल नचलाई बस अनि रिफ्रेस गर!")
