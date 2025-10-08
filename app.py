import streamlit as st
from modules.speech_to_text import transcribe_audio
from modules.gemini_backend import summarize_text, generate_quiz
from modules.file_export import export_pdf

st.set_page_config(page_title="Lecture Voice-to-Notes", layout="wide")

st.title("🎙️ Lecture Voice-to-Notes Generator")
st.write("Convert speech or recorded lectures into summarized notes.")

uploaded_file = st.file_uploader(
    "Upload your lecture recording", 
    type=["mp3", "wav", "m4a"]
)

if uploaded_file:
    # STEP 1: Transcribe Audio
    with st.spinner("🔄 Transcribing audio..."):
        try:
            transcript = transcribe_audio(uploaded_file)
        except Exception as e:
            st.error(f"Error during transcription: {e}")
            transcript = ""

    if transcript:
        # Display Transcript
        st.subheader("Transcript")
        st.text_area("Transcript", transcript, height=200)

        # STEP 2: Generate Summary
        with st.spinner("📝 Generating summary notes..."):
            summary_text = summarize_text(transcript)
            st.subheader("Summary Notes")
            summary_list = []
            if summary_text.startswith("⚠"):
                st.error(summary_text)
            else:
                summary_list = [line.strip("•- ") for line in summary_text.split("\n") if line.strip()]
                for point in summary_list:
                    st.markdown(f"- {point}")

        # STEP 3: Generate Quiz
        with st.spinner("❓ Generating quiz questions..."):
            quiz_text = generate_quiz(transcript, n=10)
            st.subheader("Quiz")
            quiz_list = []
            if quiz_text.startswith("⚠"):
                st.error(quiz_text)
            else:
                quiz_list = [q.strip() for q in quiz_text.split("\n") if q.strip()]
                for q in quiz_list:
                    st.markdown(f"• {q}")

        # STEP 4: Export to PDF
        if st.button("📄 Download as PDF"):
            if summary_list or quiz_list:
                filename = export_pdf(summary_list, quiz_list)
                with open(filename, "rb") as pdf_file:
                    st.download_button(
                        label="⬇ Download PDF",
                        data=pdf_file,
                        file_name=filename,
                        mime="application/pdf"
                    )
            else:
                st.warning("⚠ No content to export yet.")
