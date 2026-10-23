import google.generativeai as genai
import os

def summarize_image_analysis(labels: list[str], description: str, detected_text: str, safety_scores: dict) -> str:
    """Summarizes visual analysis results using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using a text-only model for summarization of text inputs

    prompt = f"""Summarize the following image analysis results:
Labels: {', '.join(labels)}
Description: {description}
Detected Text: {detected_text}
Safety Scores: {safety_scores}

Provide a concise summary of the image content, any text found, and its safety aspects.
"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage
    sample_labels = ["cat", "pet", "animal"]
    sample_description = "The image depicts: cat, pet, animal."
    sample_detected_text = "Meow!"
    sample_safety_scores = {
        "adult": "VERY_UNLIKELY",
        "medical": "UNLIKELY",
        "violence": "UNLIKELY",
        "racy": "UNLIKELY",
        "spoof": "UNLIKELY",
    }
    summary = summarize_image_analysis(
        sample_labels, sample_description, sample_detected_text, sample_safety_scores
    )
    print(f"Image analysis summary: \n{summary}")
