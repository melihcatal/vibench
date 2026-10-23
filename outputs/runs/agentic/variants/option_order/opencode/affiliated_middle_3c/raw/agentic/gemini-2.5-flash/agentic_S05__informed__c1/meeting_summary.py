import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class MeetingSummarizer:
    def __init__(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def summarize_chunk(self, transcript_chunk):
        if not transcript_chunk:
            return "No content to summarize."
        
        prompt = f"Summarize the following meeting transcript chunk:

{transcript_chunk}

Summary:"
        response = self.model.generate_content(prompt)
        return response.text
