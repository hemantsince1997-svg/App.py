import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Strong Memory)")

# २. तेरो API चाबी
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. मोडल मिलाउने
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# ४. बलियो मेमोरी सेटअप (Session State Memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ५. एआईलाई कडा निर्देशन (System Instruction जस्तै)
if "chat_session" not in st.session_state:
    # एआईलाई सुरुमै उसको भूमिका सम्झाउने
    initial_prompt = "You are a loyal friend of Hemant. Always speak in Nepali. Remember his details and be very friendly."
    st.session_state.chat_session = model.start_chat(history=[])

# ६. पुराना म्यासेज देखाउने (Scannable History)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ७. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # हेमन्तको म्यासेज सेभ गर्ने
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # मेमोरी सहितको जवाफ माग्ने
            response = st.session_state.chat_session.send_message(f"Hemant says: {prompt}. Reply in Nepali.")
            msg = response.text
            st.write(msg)
            # एआईको म्यासेज सेभ गर्ने
            st.session_state.chat_history.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भर अलि सुस्त भयो, एकपटक रिफ्रेस गरेर फेरि पठा त!")
