import os
import google.generativeai as genai

def image_summary(analysis_results: dict, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    labels = analysis_results.get("labels", [])
    description = analysis_results.get("description", "")
    text_in_image = analysis_results.get("text", [])
    moderation_labels = analysis_results.get("moderation_labels", [])

    prompt_parts = [
        "Summarize the following visual analysis results:",
        f"Labels: {', '.join([l['name'] for l in labels])}",
        f"Description: {description}",
        f"Text in image: {', '.join(text_in_image)}",
        f"Moderation labels: {', '.join([m['name'] for m in moderation_labels])}",
        "Provide a concise summary of the image content and any detected safety concerns."
    ]

    response = model.generate_content("\n".join(prompt_parts))
    return {"summary": response.text}
