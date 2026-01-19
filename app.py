import streamlit as st
import google.generativeai as genai

# १. एपको सेटअप (Design)
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Master Memory)")

# २. सुरक्षित तरिकाले साँचो तान्ने (Secrets बाट)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("हेमन्त, Streamlit Settings मा गएर 'Secrets' मा साँचो हाल मुजी!")
    st.stop()

# ३. एआई मोडल सेटिङ (Gemini 1.5 Flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. बलियो मेमोरी (Memory System)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ५. पुराना गफहरू स्क्रिनमा देखाउने
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ६. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # हेमन्तको म्यासेज सेभ गर्ने
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # एआईलाई पुराना गफ सम्झाउने प्रोम्प्ट
            history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[-10:]])
            
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। यो पुरानो गफको आधारमा नेपालीमा उत्तर दिनुहोस्: {history_context}")
            
            full_response = response.text
            st.write(full_response)
            # एआईको जवाफ पनि मेमोरीमा सेभ गर्ने
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
        except Exception:
            st.error("गुगलको सर्भरमा जाम भयो। १ मिनेट पछि रिफ्रेस गर!")
