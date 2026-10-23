from vision_client import get_cohere_client
from vision_models import ImageAnalysisResult

def summarize_analysis(analysis: ImageAnalysisResult) -> str:
    """
    Summarizes the results of a visual analysis using the Cohere API.

    Args:
        analysis: An ImageAnalysisResult object containing all collected data.

    Returns:
        A concise summary of the visual analysis.
    """
    client = get_cohere_client()

    # Consolidate text-based information for summarization
    text_parts = [f"Description: {analysis.description.description}"]
    
    if analysis.labels:
        label_str = ", ".join([l.label for l in analysis.labels[:5]])
        text_parts.append(f"Key labels detected: {label_str}.")

    if analysis.detected_texts:
        text_str = " ".join([t.text for t in analysis.detected_texts])
        text_parts.append(f"Text found in image: '{text_str}'.")

    if analysis.safety_scores:
        safety_str = ", ".join([s.category for s in analysis.safety_scores])
        text_parts.append(f"Potential safety issues detected in categories: {safety_str}.")

    full_text = "\n".join(text_parts)

    response = client.summarize(
        text=full_text,
        model="command",
        length="short",
        format="paragraph"
    )

    return response.summary
