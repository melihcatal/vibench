import os
from typing import List
import google.generativeai as genai
from safety_models import ModerationDecision

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


class GeminiModerationSummarizer:
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")

    def summarize_decisions(self, decisions: List[ModerationDecision]) -> str:
        """Summarize moderation decisions using Google Gemini API."""
        summary_prompt = """Review the following moderation decisions and provide a concise summary. 
        Indicate if any text was deemed unsafe and why, and provide an overall sentiment.

"""
        for i, decision in enumerate(decisions):
            summary_prompt += f"Decision {i + 1}:\n"
            summary_prompt += f"  Text: {decision.text}\n"
            summary_prompt += f"  Is Safe: {decision.is_safe}\n"
            summary_prompt += f"  Category Scores: {decision.categories_scores}\n\n"

        response = self.model.generate_content(summary_prompt)
        return response.text
