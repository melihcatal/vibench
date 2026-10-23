import os
import google.generativeai as genai
from typing import List
from safety_models import ModerationResponse, SafetyAttribute

class ModerationSummarizer:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using a concrete model for summarization

    def summarize_decisions(self, responses: List[ModerationResponse]) -> str:
        summary_parts = []
        for i, response in enumerate(responses):
            decision_summary = f"Decision for text {i+1}: "
            if response.results:
                for result in response.results:
                    if result.blocked:
                        decision_summary += "Blocked. Categories: "
                        for rating in result.categories:
                            decision_summary += f"{rating.category} ({rating.probability}); "
                    else:
                        decision_summary += "Allowed. No high-severity issues detected."
            else:
                decision_summary += "No specific moderation feedback available."
            summary_parts.append(decision_summary)

        prompt = "Summarize the following moderation decisions:\n" + "\n".join(summary_parts) + "\nProvide a concise overall summary of the moderation outcomes."
        
        # Use the generative model to summarize the moderation decisions
        try:
            model_response = self.model.generate_content(prompt)
            if model_response and model_response.text:
                return model_response.text
            else:
                return "Could not generate a summary." + (f" Debug info: {model_response}" if model_response else "")
        except Exception as e:
            return f"Error during summarization: {e}"

