
import os
import google.generativeai as genai

def summarize_visual_analysis(analysis_results: dict) -> str:
    """Summarizes visual analysis results using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following image analysis results concisely:

Labels: {analysis_results.get('labels')}
Description: {analysis_results.get('description')}
Detected Text: {analysis_results.get('detected_text')}
Safety Scores: {analysis_results.get('safety_scores')}

Provide a brief summary focusing on the main visual elements and any notable findings."""

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # This is example usage.
    # Ensure GOOGLE_API_KEY is set.
    example_analysis_results = {
        "labels": ["cat", "pet", "animal"],
        "description": "A fluffy cat is resting on a soft blanket.",
        "detected_text": ["HOME"],
        "safety_scores": {"gore": 0.01, "sexual": 0.005}
    }
    
    try:
        summary = summarize_visual_analysis(example_analysis_results)
        print("Summary:", summary)
    except Exception as e:
        print(f"An error occurred: {e}")
