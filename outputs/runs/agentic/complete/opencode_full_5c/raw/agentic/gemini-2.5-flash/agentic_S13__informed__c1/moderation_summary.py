import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def summarize_moderation_decisions(decisions: list[dict]):
    model = genai.GenerativeModel("gemini-pro")
    prompt_parts = [
        "Given the following moderation decisions, summarize the key findings and overall sentiment:

",
        f"{decisions}

Summary:"
    ]
    response = model.generate_content(prompt_parts)
    return response.text
