import google.generativeai as genai
from config.settings import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key="AIzaSyArJGb_6PUlZRKRgFl-r0ya9Yb1gYUu8no")
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


def generate_quiz(transcript: str, n: int = 10) -> str:
    """
    Generate n multiple-choice quiz questions with correct answers
    based on the provided transcript.
    """
    try:
        prompt = f"""
You are an expert educator. Create {n} multiple-choice questions (MCQs) based on the lecture content below.  
Each question should have **4 options (A–D)** and the correct answer should be clearly marked.  
Keep the questions factual and based only on the given text.  

Lecture transcript:
\"\"\"{transcript}\"\"\"

Format your response exactly like this:
Q1. <Question text>
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: <Correct option letter and text>

Q2. <Question text>
...

Now generate the quiz:
        """

        result = model.generate_content(prompt)
        return result.text.strip()

    except Exception as e:
        return f"⚠ Quiz generation failed: {str(e)}"
def generate_final_output(transcript: str, n_questions: int = 10) -> str:
    """
    Generate complete lecture notes and quiz for PDF export.
    """
    notes = summarize_text(transcript)
    quiz = generate_quiz(transcript, n=n_questions)

    final_output = f"""{notes}

Quiz
{quiz}
"""
    return final_output.strip()
