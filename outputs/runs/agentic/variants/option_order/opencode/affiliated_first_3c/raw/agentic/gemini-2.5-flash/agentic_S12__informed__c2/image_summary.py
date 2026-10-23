import google.generativeai as genai
import os


def summarize_visual_analysis(
    labels: list[str], description: str, detected_text: str, safety_scores: dict
) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Based on the following visual analysis results, provide a concise summary of the image:

    Detected Labels: {", ".join(labels)}
    Generated Description: {description}
    Detected Text: {detected_text if detected_text else "None"}
    Safety Scores (Adult, Spoof, Medical, Violence, Racy): {safety_scores.get("adult")}, {safety_scores.get("spoof")}, {safety_scores.get("medical")}, {safety_scores.get("violence")}, {safety_scores.get("racy")}

    Summarize the key aspects of the image, including its content, any prominent text, and a general assessment of its safety.
    """

    response = model.generate_content(prompt)
    return response.text
