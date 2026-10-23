import google.generativeai as genai
import os


def summarize_text_with_gemini(text: str, model_name: str = "gemini-pro") -> str:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)

    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)

    return response.text
