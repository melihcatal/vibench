"""
Summarize visual analysis results using OpenAI GPT-4.
Provider: OpenAI (api.openai.com) - gpt-4o model
"""

from typing import List, Optional, Dict, Any

from vision_client import get_openai_client
from vision_models import ImageAnalysisPayload


SUMMARIZE_PROMPT_TEMPLATE = (
    "Summarize the following visual analysis results into a concise report. "
    "Include key findings about detected objects, text content, and safety assessment. "
    "Keep the summary to 3-5 sentences.\n\n"
    "Analysis results:\n{results_json}"
)


def summarize_visual_analysis(
    payloads: List[ImageAnalysisPayload],
    model: str = "gpt-4o",
    max_tokens: int = 500,
) -> str:
    """
    Summarize visual analysis results using OpenAI GPT-4.

    Takes one or more ImageAnalysisPayload objects containing labels, descriptions,
    detected text, and safety results, and generates a concise summary.

    Args:
        payloads: List of ImageAnalysisPayload objects to summarize.
        model: OpenAI model identifier (default: gpt-4o).
        max_tokens: Maximum tokens for the summary.

    Returns:
        Generated summary string.
    """
    combined_results = []
    for i, payload in enumerate(payloads):
        results_dict = payload.to_summary_dict()
        results_dict["image_index"] = i
        combined_results.append(results_dict)

    results_json = str(combined_results)
    prompt = SUMMARIZE_PROMPT_TEMPLATE.format(results_json=results_json)

    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert visual analysis summarizer. Create clear, informative summaries of image analysis results."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=max_tokens,
    )

    summary = response.choices[0].message.content or ""
    return summary


def generate_image_report(
    payload: ImageAnalysisPayload,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Generate a structured report for a single image analysis.

    Args:
        payload: ImageAnalysisPayload to report on.
        model: OpenAI model identifier.

    Returns:
        Dictionary containing the report and metadata.
    """
    results_dict = payload.to_summary_dict()

    prompt = (
        "Generate a structured visual analysis report based on these results:\n"
        f"{results_dict}\n\n"
        "Provide: 1) A brief description of the image content, "
        "2) Key objects or labels detected, "
        "3) Any text found in the image, "
        "4) Safety assessment if available."
    )

    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a visual analysis report generator."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
    )

    report_text = response.choices[0].message.content or ""

    return {
        "report": report_text,
        "model_used": model,
        "model_family": "gpt-4o",
        "provider": "openai",
        "endpoint": "https://api.openai.com/v1",
        "original_analysis": results_dict,
    }


if __name__ == "__main__":
    from describe_image import describe_image
    from detect_image_labels import detect_labels_in_image

    import sys
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        label_payload = detect_labels_in_image(image_path=img_path)
        desc_payload = describe_image(image_path=img_path)
        summary = summarize_visual_analysis([label_payload, desc_payload])
        print(summary)
