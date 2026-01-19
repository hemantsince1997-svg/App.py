import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Master)")

# २. तेरो नयाँ API चाबी (Fresh Key)
API_KEY = "AIzaSyDzbJZAYNyq-sflLBIk3PUyDERoBuFW9bw"
genai.configure(api_key=API_KEY)

# ३. एआई मोडल र फिल्टर सेटिङ (No Restrictions)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)

# ४. स्मरणशक्ति (Memory) सुरक्षित राख्ने
if "messages" not in st.session_state:
    st.session_state.messages = []

# ५. पुराना गफहरू देखाउने
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
            # एआईलाई दिइने कडा निर्देशन
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। जहिले पनि नेपालीमा रमाइलो जवाफ दिनुहोस्। हेमन्तले भन्यो: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भर अलि बिजी भयो मुजी, १ मिनेट पछि रिफ्रेस गरेर फेरि पठा त!")
