import streamlit as st
from openai import OpenAI
import gspread
from google.oauth2.service_account import Credentials

# १. एआई सेटअप
st.title("My Personal AI (Cloud Memory)")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# २. गुगल सिट (Cloud) कनेक्ट - यसले गर्दा फोन हराए पनि डाटा बच्छ
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
gc = gspread.authorize(creds)
sh = gc.open("MyAIMemory").sheet1 # तेरो गुगल सिटको नाम 'MyAIMemory' हुनुपर्छ

# ३. च्याट मेमोरी लोड गर्ने
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ४. नयाँ म्यासेज र क्लाउड सेभ
if prompt := st.chat_input("भन के छ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ChatGPT बाट जवाफ लिने (संसारको ज्ञान)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a best friend who remembers everything."}] + st.session_state.messages
    )
    ans = response.choices[0].message.content
    
    with st.chat_message("assistant"):
        st.markdown(ans)
    
    st.session_state.messages.append({"role": "assistant", "content": ans})
    
    # क्लाउड (Google Sheet) मा डाटा पठाउने
    sh.append_row([prompt, ans])
