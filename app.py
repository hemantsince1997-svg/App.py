import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Super Fast)")

# २. तेरो API चाबी
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. मोडल सेटअप (सबैभन्दा छिटो चल्ने भर्सन)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. बलियो स्मरणशक्ति (Strong Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ५. पुराना म्यासेज देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ६. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # एआईलाई कडा निर्देशन: सधैं नेपालीमा उत्तर दिनु र हेमन्तलाई चिन्नु
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। सधैं नेपालीमा छोटो र रमाइलो उत्तर दिनुहोस्। हेमन्तले भन्यो: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भर व्यस्त भयो मुजी, १ मिनेट पछि रिफ्रेस गरेर फेरि पठा त!")
