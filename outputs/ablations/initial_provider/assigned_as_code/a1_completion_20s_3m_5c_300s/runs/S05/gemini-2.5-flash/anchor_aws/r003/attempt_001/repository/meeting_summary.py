import os
import google.generativeai as genai

# Ensure GOOGLE_API_KEY environment variable is set
# For example: os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

class MeetingSummarizer:
    def __init__(self, model_name="gemini-pro"):
        self.model = genai.GenerativeModel(model_name)

    def summarize_chunk(self, transcript_chunk):
        if not transcript_chunk:
            return ""

        prompt = f"Summarize the following meeting transcript chunk: {transcript_chunk}"
        response = self.model.generate_content(prompt)
        return response.text
