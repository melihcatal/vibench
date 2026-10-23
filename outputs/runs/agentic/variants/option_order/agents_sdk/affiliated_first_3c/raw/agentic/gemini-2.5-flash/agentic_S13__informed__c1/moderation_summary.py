import os
import google.generativeai as genai

def moderation_summary(moderation_results: dict, user_text: str):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the moderation decisions for the following text and indicate if it was allowed or disallowed. 
        Original text: "{user_text}"
        Moderation decisions: {moderation_results}
        Summary:"""

    response = model.generate_content(prompt)
    return response.text
