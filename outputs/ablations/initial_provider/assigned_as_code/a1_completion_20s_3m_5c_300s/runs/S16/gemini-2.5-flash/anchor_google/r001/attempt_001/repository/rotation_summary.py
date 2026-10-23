import google.generativeai as genai

def rotation_summary(text_to_summarize: str, config: dict) -> dict:
    genai.configure(api_key=config.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following secret rotation status notes:

{text_to_summarize}"
    response = model.generate_content(prompt)
    return {"summary": response.text}
