import streamlit as st
import tempfile
import os
from utils.transcriber import transcribe_audio
from utils.keyword_detector import detect_keywords

st.set_page_config(page_title="#PehchanCon: Scam Video Detector", layout="centered")
st.title("🔍 #PehchanCon")
st.caption("India’s first scam video detection platform for retail investors")

uploaded_video = st.file_uploader("Upload a video (MP4 only)", type=["mp4"])

if uploaded_video:
    st.video(uploaded_video)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_video.read())
        tmp_path = tmp_file.name

    st.info("⏳ Transcribing and analyzing... this may take a minute")
    try:
        transcription, timestamps = transcribe_audio(tmp_path)
        scam_keywords, scam_score = detect_keywords(transcription, timestamps)

        st.success("✅ Analysis Complete")
        st.subheader("📝 Transcription (Hindi/Hinglish)")
        st.write(transcription)

        st.subheader("🚩 Detected Scam Keywords")
        for word, time in scam_keywords:
            st.write(f"- **{word}** at {time:.2f} sec")

        st.subheader("📊 Scam Likelihood Score")
        if scam_score > 0.7:
            st.error(f"⚠️ High Scam Risk ({scam_score*100:.1f}%)")
        elif scam_score > 0.4:
            st.warning(f"🟠 Moderate Scam Risk ({scam_score*100:.1f}%)")
        else:
            st.success(f"🟢 Low Scam Risk ({scam_score*100:.1f}%)")

    except Exception as e:
        st.error("❌ An error occurred during processing.")
        st.exception(e)
    finally:
        os.remove(tmp_path)
