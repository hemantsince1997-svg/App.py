import streamlit as st
import google.generativeai as genai

# १. एपको नाम र सेटिङ
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. Streamlit Secrets बाट साँचो तान्ने (सुरक्षित तरिका)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("ओए हेमन्त, Streamlit 'Secrets' मा साँचो हाल मुजी!")
    st.stop()

# ३. एआई मोडल सेटअप
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. मेमोरी (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ५. पुराना गफहरू देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ६. म्यासेज पठाउने ठाउँ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # सिधै उत्तर माग्ने (सफा र छिटो)
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। नेपालीमा छोटो जवाफ दिनुहोस्। प्रश्न: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलले अझै टेरेन मुजी! एकछिन पछि रिफ्रेस गर।")
