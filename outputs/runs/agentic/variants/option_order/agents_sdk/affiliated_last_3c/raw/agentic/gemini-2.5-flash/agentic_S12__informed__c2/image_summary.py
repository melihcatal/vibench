import os
import google.generativeai as genai

def summarize_visual_analysis_results(analysis_results: dict) -> str:
    """Summarizes visual analysis results using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    labels = analysis_results.get("labels", [])
    description = analysis_results.get("description", "")
    detected_text = analysis_results.get("detected_text", [])
    safety_scores = analysis_results.get("safety_scores", {})

    prompt_parts = [
        "Given the following visual analysis results:",
        f"- Detected labels: {', '.join(labels) if labels else 'None'}",
        f"- Image description: {description if description else 'None'}",
        f"- Detected text: {', '.join(detected_text) if detected_text else 'None'}",
        f"- Safety scores: {safety_scores if safety_scores else 'None'}",
        "Please provide a concise summary of the image, highlighting key visual elements and any notable aspects.",
        "Keep the summary to 2-3 sentences."
    ]

    response = model.generate_content("\n".join(prompt_parts))
    return response.text

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_API_KEY environment variable is set
    sample_analysis_results = {
        "labels": ["cat", "pet", "animal", "domestic cat"],
        "description": "The image appears to show: cat, pet, animal, domestic cat.",
        "detected_text": ["Cute Cat"],
        "safety_scores": {"adult": "VERY_UNLIKELY", "violence": "VERY_UNLIKELY", "racy": "UNLIKELY"}
    }

    try:
        summary = summarize_visual_analysis_results(sample_analysis_results)
        print(f"Image Summary: {summary}")
    except Exception as e:
        print(f"Error summarizing analysis results: {e}")
        print("Please ensure GOOGLE_API_KEY environment variable is set.")
