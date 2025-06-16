
import streamlit as st
from utils.transcriber import transcribe_audio
from utils.keyword_detector import detect_keywords

st.title("📽️ PehchanCon – Scam Detection for Investment Videos")

uploaded_file = st.file_uploader("Upload a short video (MP4, 2 mins max)", type=["mp4"])

if uploaded_file:
    st.video(uploaded_file)
    st.info("Transcribing and scanning for scam words...")

    transcript = transcribe_audio(tmp_path) 
    keywords, timestamps = detect_keywords(transcript)

    st.subheader("📝 Transcript:")
    st.text(transcript)

    st.subheader("⚠️ Scam Keywords Detected:")
    for word, ts in zip(keywords, timestamps):
        st.markdown(f"- **{word}** at `{ts}`")
