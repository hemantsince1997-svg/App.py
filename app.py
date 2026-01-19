import streamlit as st
import google.generativeai as genai

# १. एपको मुख्य सेटिङ
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Final Recovery)")

# २. तेरो ताजा API Key
API_KEY = "AIzaSyDzbJZAYNyq-sflLBIk3PUyDERoBuFW9bw"
genai.configure(api_key=API_KEY)

# ३. मोडल र सुरक्षा सेटिङ (Zero Restrictions)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. मेमोरी व्यवस्थापन (यसले गर्दा ह्याङ्ग हुँदैन)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ५. पुराना गफहरू सफा देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ६. मुख्य गफगाफ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # एकदमै छोटो र छिटो उत्तर माग्ने
            response = model.generate_content(f"तपाईं हेमन्तको जिग्री साथी हो। छोटो मिठो नेपालीमा मात्र बोल्नुहोस्। प्रश्न: {prompt}")
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception:
            st.error("ओए हेमन्त, गुगलको सिस्टमले अझै दुख दिँदैछ। १० मिनेट कतै घुमेर आइज अनि रिफ्रेस गर्, बल्ल चल्छ!")
