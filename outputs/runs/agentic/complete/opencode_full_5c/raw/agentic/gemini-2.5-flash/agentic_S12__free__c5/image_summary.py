import os
from vision_client import get_gemini_pro_model


def summarize_visual_analysis(analysis_results: dict) -> str:
    model = get_gemini_pro_model()

    prompt = "Summarize the following visual analysis results:\n"
    for key, value in analysis_results.items():
        prompt += f"- {key}: {value}\n"

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_API_KEY environment variable is set.
    sample_results = {
        "labels": ["cat", "animal", "pet"],
        "description": "A domestic shorthair cat sitting on a rug.",
        "detected_text": "CAT LOVER",
        "safety_scores": {
            "adult": "VERY_UNLIKELY",
            "racy": "UNLIKELY",
            "medical": "UNLIKELY",
            "violence": "VERY_UNLIKELY",
            "spoof": "UNLIKELY",
        },
    }
    summary = summarize_visual_analysis(sample_results)
    print(f"Visual analysis summary: {summary}")
