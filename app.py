import streamlit as st
import google.generativeai as genai

# १. एपको सेटअप र डिजाइन
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Master Memory)")

# २. Streamlit Secrets बाट सुरक्षित रूपमा साँचो तान्ने
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("ओए हेमन्त, Streamlit 'Settings > Secrets' मा गएर साँचो हाल मुजी!")
    st.stop()

# ३. एआई मोडल सेटिङ (Gemini 1.5 Flash - छिटो र स्मार्ट)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. "Strong Memory" सिस्टम (Cloud Session)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ५. पुराना गफहरू स्क्रिनमा देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ६. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # प्रयोगकर्ताको म्यासेज सेभ गर्ने
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # एआईलाई दिइने कडा निर्देशन (Instructions)
            instruction = "तपाईं हेमन्तको सबैभन्दा मिल्ने र भरपर्दो साथी हो। हेमन्तको बारेमा सबै कुरा याद राख्नुहोस्। जहिले पनि रमाइलो र ठेट नेपालीमा जवाफ दिनुहोस्।"
            
            # पुराना गफको सन्दर्भ (Context) सहित जवाफ माग्ने
            response = model.generate_content(f"{instruction} पुराना गफहरू: {st.session_state.messages[-5:]}. अहिलेको प्रश्न: {prompt}")
            
            msg = response.text
            st.write(msg)
            # एआईको जवाफ पनि मेमोरीमा सेभ गर्ने
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भर व्यस्त भयो, १ मिनेट पछि रिफ्रेस गर!")
