import streamlit as st
import google.generativeai as genai
import time

# १. एप सेटअप र नाम
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Turbo)")

# २. तेरो API चाबी
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. मोडल सेटअप
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# ४. स्मरणशक्ति (Strong Memory) सेटअप
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ५. पुराना गफगाफ देखाउने
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ६. गफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # एआईलाई जवाफ दिन लगाउने (३ पटकसम्म प्रयास गर्ने जुक्ति)
        for attempt in range(3):
            try:
                instruction = f"तपाईं हेमन्तको जिग्री साथी हो। जहिले पनि नेपालीमा मात्र बोल्नुहोस्। हेमन्तले भन्यो: {prompt}"
                response = st.session_state.chat_session.send_message(instruction)
                full_response = response.text
                message_placeholder.write(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                break
            except Exception:
                if attempt < 2:
                    time.sleep(2) # २ सेकेन्ड कुरेर फेरि प्रयास गर्ने
                    continue
                else:
                    st.error("गुगलको सर्भर एकदमै व्यस्त छ मुजी, १ मिनेट पछि पेज रिफ्रेस गरेर पठा त!")
