import os
import google.generativeai as genai

def summarize_image_analysis(analysis_results: dict) -> str:
    """Summarizes visual analysis results using the Gemini API.

    Args:
        analysis_results: A dictionary containing various analysis results
                          (e.g., labels, description, texts, safety_scores).

    Returns:
        A string summary of the image analysis.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = "Summarize the following image analysis results in a concise paragraph:\n\n"
    for key, value in analysis_results.items():
        prompt += f"{key.replace('_', ' ').title()}: {value}\n"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    # Example usage
    example_results = {
        "image_uri": "gs://cloud-samples-data/vision/label/wakeupcat.jpg",
        "labels": ["cat", "pet", "whiskers"],
        "description": "An image featuring cat, pet, whiskers.",
        "texts": [],
        "safety_scores": {
            "adult": "VERY_UNLIKELY",
            "spoof": "UNLIKELY",
            "medical": "POSSIBLE",
            "violence": "UNLIKELY",
            "racy": "UNLIKELY"
        }
    }
    print("Generating summary for example results:")
    summary = summarize_image_analysis(example_results)
    print(summary)
