import streamlit as st
import google.generativeai as genai

# १. एपको नाम र सेटिङ
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. तेरो नयाँ चाबी सिधै कोडमा हाल्दिएको छु
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ३. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # एआईलाई नेपालीमा मात्र बोल्न लगाउने
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। सधैं नेपालीमा उत्तर दिनुहोस्। हेमन्तले भन्यो: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error("अझै चलेन! कृपया Requirements फाइल चेक गर्नुहोस्।")
