# modules/speech_to_text.py
import whisper
import numpy as np
from pydub import AudioSegment
import io

# Load Whisper model once
model = whisper.load_model("base")  # or "small", "medium", "large" depending on your needs

def transcribe_audio(file) -> str:
    """
    Transcribe uploaded audio (mp3/m4a/wav) into text.
    This function is ffmpeg-free and works in-memory.
    
    Args:
        file: BytesIO or file-like object uploaded by Streamlit
    
    Returns:
        transcript text
    """
    try:
        # Convert audio to WAV in-memory
        audio = AudioSegment.from_file(io.BytesIO(file.read()))
        audio = audio.set_channels(1).set_frame_rate(16000)  # Mono, 16kHz for Whisper

        # Convert to NumPy array
        samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0

        # Transcribe with Whisper
        result = model.transcribe(samples, fp16=False)
        return result["text"]
    
    except Exception as e:
        return f"⚠ Error during transcription: {e}"
