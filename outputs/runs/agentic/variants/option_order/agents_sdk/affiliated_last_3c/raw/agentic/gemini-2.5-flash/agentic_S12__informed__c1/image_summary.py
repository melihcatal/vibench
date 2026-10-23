import google.generativeai as genai
import os
from typing import Dict, Any

def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """Summarizes visual analysis results using the Google Gemini API.

    Args:
        analysis_results: A dictionary containing various image analysis outputs
                          (e.g., labels, description, detected_text, safety_scores).

    Returns:
        A string summary of the analysis results.
    """
    # Ensure GOOGLE_API_KEY environment variable is set.
    # Example: os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Use a specific model that supports text generation
    model = genai.GenerativeModel('gemini-pro') # Or 'gemini-1.0-pro' or similar

    prompt = f"""Summarize the following image analysis results concisely:
Image URI: {analysis_results.get('image_uri', 'N/A')}
Labels: {', '.join(analysis_results.get('labels', []))}
Description: {analysis_results.get('description', 'N/A')}
Detected Text: {analysis_results.get('detected_text', 'N/A')}
Safety Scores: {analysis_results.get('safety_scores', 'N/A')}

Provide a short, easy-to-understand summary. Highlight any notable findings, especially regarding safety.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    # Example usage (replace with actual analysis results)
    # Make sure to set GOOGLE_API_KEY environment variable
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
    
    sample_results = {
        "image_uri": "gs://my-bucket/image.jpg",
        "labels": ["cat", "pet", "animal", "mammal"],
        "description": "An image of a cat sitting on a couch.",
        "detected_text": "",
        "safety_scores": {
            "adult": "VERY_UNLIKELY",
            "spoof": "UNLIKELY",
            "medical": "UNLIKELY",
            "violence": "UNLIKELY",
            "racy": "UNLIKELY"
        }
    }
    
    if "GOOGLE_API_KEY" in os.environ:
        summary = summarize_visual_analysis(sample_results)
        print("\n--- Image Analysis Summary ---")
        print(summary)
    else:
        print("Please set the GOOGLE_API_KEY environment variable to run this example.")
