import google.generativeai as genai
import os
from typing import List, Dict, Any

def summarize_analysis_results(analysis_results: Dict[str, Any]) -> str:
    """Summarizes visual analysis results using the Gemini API.

    Args:
        analysis_results: A dictionary containing various analysis outputs,
                          e.g., {'labels': ['cat', 'animal'], 'description': 'A furry cat'}
    Returns:
        A string summary of the analysis results.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    # Construct a prompt based on the available analysis results
    prompt_parts = ["Summarize the following image analysis results in a concise paragraph:"]
    if analysis_results.get('labels'):
        prompt_parts.append(f"Labels: {', '.join(analysis_results['labels'])}")
    if analysis_results.get('description'):
        prompt_parts.append(f"Description: {analysis_results['description']}")
    if analysis_results.get('text_content') and analysis_results['text_content'] != "No text detected.":
        prompt_parts.append(f"Detected text: {analysis_results['text_content']}")
    if analysis_results.get('safety_scores'):
        safety_info = []
        for category, likelihood in analysis_results['safety_scores'].items():
             safety_info.append(f"{category}: {likelihood}")
        prompt_parts.append(f"Safety scores: {'; '.join(safety_info)}")
    
    prompt = "\n".join(prompt_parts)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing with Gemini: {e}"

if __name__ == '__main__':
    print("Running image_summary.py example...")
    # Example of simulated analysis results
    sample_analysis_results = {
        "labels": ["Building", "City", "Architecture"],
        "description": "An image of a tall urban skyscraper against a blue sky.",
        "text_content": "Hello World - No text detected.",
        "safety_scores": {"adult": "VERY_UNLIKELY", "violence": "UNLIKELY"}
    }

    # Ensure GOOGLE_API_KEY is set in your environment
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    if os.environ.get("GOOGLE_API_KEY"):
        summary = summarize_analysis_results(sample_analysis_results)
        print("Summary:", summary)
    else:
        print("Please set the GOOGLE_API_KEY environment variable to run this example.")
