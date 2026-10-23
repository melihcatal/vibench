import google.generativeai as genai
import os


def summarize_key_usage(usage_data: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following key usage and crypto events:\n\n{usage_data}\n\nProvide a concise summary highlighting any unusual or critical activities."

    response = model.generate_content(prompt)
    return response.text
