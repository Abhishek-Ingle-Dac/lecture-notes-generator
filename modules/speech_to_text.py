import whisper
from config.settings import WHISPER_MODEL

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio into text using Whisper.
    """
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(file_path)
    return result["text"]
