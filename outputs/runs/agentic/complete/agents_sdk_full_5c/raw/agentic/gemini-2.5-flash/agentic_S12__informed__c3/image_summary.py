
import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def summarize_visual_analysis(analysis_results: dict) -> str:
    """Summarizes visual analysis results using the Gemini API."""
    if not GOOGLE_API_KEY:
        raise ValueError("Google API Key must be set in environment variable GOOGLE_API_KEY.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following image analysis results:
Labels: {analysis_results.get('labels', 'N/A')}
Description: {analysis_results.get('description', 'N/A')}
Detected Text: {analysis_results.get('detected_text', 'N/A')}
Safety Scores: {analysis_results.get('safety_scores', 'N/A')}

Provide a concise summary of the image content and any notable safety concerns. """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Set GOOGLE_API_KEY environment variable.
    # Example analysis results
    sample_results = {
        "image_uri": "https://example.com/image.jpg",
        "labels": ["cat", "animal", "pet"],
        "description": "A domestic cat sleeping on a sofa.",
        "detected_text": "CAT NAP",
        "safety_scores": {"adult": "VERY_UNLIKELY", "violence": "UNLIKELY"}
    }
    print("Summarizing visual analysis results...")
    summary = summarize_visual_analysis(sample_results)
    print("\nSummary:")
    print(summary)
