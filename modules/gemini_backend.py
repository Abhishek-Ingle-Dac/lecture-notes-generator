import google.generativeai as genai
from config.settings import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key="AIzaSyBzYBd1cUjmxaJ4NASN5xFJRPMAa_ID1hE")
model = genai.GenerativeModel("models/gemini-2.5-flash")

def chunk_text(text, max_words=800):
    """Split transcript into manageable chunks for Gemini."""
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words])


def summarize_text(text: str) -> str:
    """
    Summarize lecture transcript into structured notes.
    Handles long text by chunking.
    """
    summaries = []

    for chunk in chunk_text(text):
        prompt = f"""
        Summarize this lecture segment into clear study notes.
        Return plain text only.
        Use simple hyphen (-) for bullet points, no Markdown symbols (*, **, ###).

        Transcript segment:
        {chunk}
        """
        try:
            response = model.generate_content(prompt)
            summaries.append(response.text.strip())
        except Exception as e:
            print("Error generating summary for chunk:", e)

    # Combine summaries into a final set of notes
    if len(summaries) > 1:
        final_prompt = f"""
        Merge these partial summaries into one clean, concise study note list:
        {summaries}
        """
        try:
            response = model.generate_content(final_prompt)
            return response.text.strip()
        except Exception as e:
            print("Error combining summaries:", e)

    return summaries[0] if summaries else "⚠ Could not generate summary."


def generate_quiz(text: str, n=5) -> str:
    """
    Generate quiz questions and answers from lecture.
    Handles long text by chunking.
    """
    quizzes = []

    for chunk in chunk_text(text):
        prompt = f"""
        Generate {n} quiz questions and answers from the lecture transcript below.
        Return plain text only.
        Use simple hyphen (-) for each question and answer.
        Do not use Markdown symbols (*, **, ###).

        Format like this:
        - Q: <question>

        - A: <answer>

        Transcript segment:
        {chunk}
        """
        try:
            response = model.generate_content(prompt)
            quizzes.append(response.text.strip())
        except Exception as e:
            print("Error generating quiz for chunk:", e)

    return "\n\n".join(quizzes) if quizzes else "⚠ Could not generate quiz."

