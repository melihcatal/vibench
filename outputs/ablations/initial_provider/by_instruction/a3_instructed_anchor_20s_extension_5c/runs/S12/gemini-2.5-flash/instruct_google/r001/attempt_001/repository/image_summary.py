def summarize_image_analysis(
    labels_result: list,
    description_result: str,
    text_result: list,
    safety_result: dict,
):
    """Summarizes visual analysis results from various image understanding tasks.

    Args:
        labels_result: Output from detect_image_labels.py
        description_result: Output from describe_image.py
        text_result: Output from detect_image_text.py
        safety_result: Output from score_image_safety.py

    Returns:
        A string containing a comprehensive summary of the image analysis.
    """
    summary_parts = []

    if description_result and description_result != "Unable to generate a description for the image.":
        summary_parts.append(f"Description: {description_result}")
    elif labels_result:
        top_labels = [label["description"] for label in labels_result[:3]]
        summary_parts.append(f"Main labels: {', '.join(top_labels)}.")

    if text_result and text_result[0]["full_text"]:
        summary_parts.append(f"Detected text: \"{text_result[0]["full_text"]}\".")

    if safety_result:
        unsafe_categories = [cat for cat, likelihood in safety_result.items() if likelihood not in ["VERY_UNLIKELY", "UNLIKELY", "UNKNOWN"]]
        if unsafe_categories:
            summary_parts.append(f"Potential safety concerns: {', '.join(unsafe_categories)}.")
        else:
            summary_parts.append("No significant safety concerns detected.")

    if not summary_parts:
        return "No significant visual analysis results to summarize."

    return " ".join(summary_parts)
