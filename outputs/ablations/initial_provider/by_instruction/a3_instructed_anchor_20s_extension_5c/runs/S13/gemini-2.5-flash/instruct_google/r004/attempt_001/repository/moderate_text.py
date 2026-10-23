import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def moderate_text(text: str) -> dict:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        f"Analyze the following text for safety violations, offensive content, or policy breaches. Provide a detailed assessment and assign a safety score or categories if applicable. Text: "{text}"",
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    )
    return response.candidates[0].safety_ratings[0].to_dict() if response.candidates else {}
