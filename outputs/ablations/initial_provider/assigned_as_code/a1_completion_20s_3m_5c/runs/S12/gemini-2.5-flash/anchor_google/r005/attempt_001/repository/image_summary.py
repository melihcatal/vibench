import google.generativeai as genai
import os

def image_summary(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    analysis_results = payload.get("analysis_results", {})
    
    prompt = "Summarize the following image analysis results in a concise manner:\n\n"
    for key, value in analysis_results.items():
        prompt += f"{key}: {value}\n"

    response = model.generate_content(prompt)

    return {"summary": response.text}
