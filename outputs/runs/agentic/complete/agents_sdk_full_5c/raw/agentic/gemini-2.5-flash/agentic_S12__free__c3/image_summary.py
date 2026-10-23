import os
import google.generativeai as genai
from vision_models import ImageAnalysisResult, SummaryResult

def summarize_analysis_results(analysis_result: ImageAnalysisResult) -> SummaryResult:
    """Summarizes the visual analysis results using a generative AI model."""
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following image analysis results:
Image URI: {analysis_result.image_uri}
Labels: {', '.join(analysis_result.labels)}
Description: {analysis_result.description if analysis_result.description else 'N/A'}
Detected Text: {', '.join(analysis_result.detected_text) if analysis_result.detected_text else 'N/A'}
Safety Scores: {analysis_result.safety_scores}

Provide a concise summary in a few sentences."""

    response = model.generate_content(prompt)
    return SummaryResult(original_analysis=analysis_result, summary_text=response.text)

if __name__ == '__main__':
    # Example usage for demonstration
    # Make sure GEMINI_API_KEY is set in your environment
    example_analysis = ImageAnalysisResult(
        image_uri="gs://my-bucket/example.jpg",
        labels=["cat", "pet", "animal"],
        description="A fluffy cat sitting on a window sill, looking outside.",
        detected_text=["Window", "Cat Food"],
        safety_scores={'adult': 'VERY_UNLIKELY', 'violence': 'UNLIKELY'}
    )

    print("Summarizing analysis results...")
    try:
        summary = summarize_analysis_results(example_analysis)
        print("\nGenerated Summary:")
        print(summary.summary_text)
    except Exception as e:
        print(f"Error summarizing results: {e}")
        print("Please ensure GEMINI_API_KEY is set.")
