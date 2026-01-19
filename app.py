import streamlit as st
import google.generativeai as genai

# १. एपको सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Secure)")

# २. साँचो लुकाउने प्रविधि (Streamlit Secrets बाट तान्ने)
try:
    # यसले सिधै तेरो Streamlit को Settings बाट साँचो तान्छ
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.warning("हेमन्त, Streamlit को 'Settings > Secrets' मा गएर साँचो हाल मुजी!")
    st.stop()

# ३. एआई मोडल सेटअप
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. पुराना गफहरू सुरक्षित राख्ने (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. नयाँ गफ सुरु गर्ने
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। रमाइलो पारामा नेपालीमा उत्तर दिनुहोस्। हेमन्तले भन्यो: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भरमा समस्या आयो, १ मिनेट पछि 'Refresh' गर!")
