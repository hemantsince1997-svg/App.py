import streamlit as st
import google.generativeai as genai

# १. सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. API चाबी
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. एआईलाई कडा निर्देशन र खुल्ला फिल्टर
# यसले गर्दा गुगलले म्यासेज रोक्ने सम्भावना कम हुन्छ
generation_config = {"temperature": 0.9, "top_p": 1, "max_output_tokens": 2048}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)

# ४. गफगाफ सेभ गर्ने (Cloud Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"तपाईं हेमन्तको जिग्री साथी हो। जहिले पनि नेपालीमा मात्र बोल्नुहोस्। हेमन्तले भन्यो: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("मुजी गुगलले अझै रोकिरहेको छ! १ मिनेट कुरेर पेज 'Refresh' गर अनि सामान्य कुरा सोध त।")
