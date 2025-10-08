# modules/speech_to_text.py
import whisper
import numpy as np
import soundfile as sf
import io
import librosa

# Load Whisper model once
model = whisper.load_model("base")

def transcribe_audio(file) -> str:
    """
    Transcribe uploaded audio (wav/flac/mp3 if ffmpeg available) without ffmpeg dependency.
    Args:
        file: BytesIO or file-like object uploaded by Streamlit
    Returns:
        transcript text
    """
    try:
        file.seek(0)

        # Read audio into numpy array
        data, sr = sf.read(io.BytesIO(file.read()))
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)  # Convert to mono

        # Resample to 16kHz
        audio_16k = librosa.resample(data, orig_sr=sr, target_sr=16000)

        # Convert to float32 (Whisper requires this)
        audio_16k = audio_16k.astype(np.float32)

        # Transcribe
        result = model.transcribe(audio_16k, fp16=False)
        return result.get("text", "")

    except Exception as e:
        return f"⚠ Error during transcription: {e}"
