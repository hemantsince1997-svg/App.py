import streamlit as st
import google.generativeai as genai
import time

# १. पेज सेटअप
st.set_page_config(page_title="हेमन्तको AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI (Non-Stop)")

# २. तेरो ताजा API चाबी
API_KEY = "AIzaSyDzbJZAYNyq-sflLBIk3PUyDERoBuFW9bw"
genai.configure(api_key=API_KEY)

# ३. एआई मोडल (बढी सहनशील सेटिङ)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. गफगाफको इतिहास (Cloud Memory)
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
        # जवाफ ल्याउन ५ पटकसम्म प्रयास गर्ने जादुई कोड
        success = False
        for i in range(5):
            try:
                response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। जस्तो सुकै प्रश्न आए पनि नहडबडाई नेपालीमा उत्तर दिनुहोस्। हेमन्तले भन्यो: {prompt}")
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                success = True
                break
            except:
                time.sleep(2) # २ सेकेन्ड कुरेर फेरि प्रयास गर्ने
        
        if not success:
            st.error("गुगलले अझै टेरेन मुजी! ५ मिनेट मोबाइल गोजीमा हाल अनि पछि 'Refresh' गरेर 'हेलो' भन् त।")
