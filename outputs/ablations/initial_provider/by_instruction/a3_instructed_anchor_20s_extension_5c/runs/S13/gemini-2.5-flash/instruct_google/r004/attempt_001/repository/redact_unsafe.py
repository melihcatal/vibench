import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def redact_unsafe(text: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        f"Identify any unsafe or policy-violating content in the following text and provide a redacted version. If no unsafe content is found, return the original text. Text: "{text}"",
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    )
    # Assuming the model returns the redacted text directly in the response
    return response.text if response.candidates else text
