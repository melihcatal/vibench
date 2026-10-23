def summarize_image_analysis(labels_data, description_data, text_data, safety_data):
    summary = {
        "labels": labels_data.get("labels", []),
        "description": description_data.get("description", "No description."),
        "detected_text": text_data.get("texts", []),
        "safety_scores": safety_data,
        "overall_assessment": "Image analysis complete.",
    }

    if safety_data:
        unsafe_categories = [
            k for k, v in safety_data.items() if v in [4, 5]
        ]  # Assuming LIKELY or VERY_LIKELY are scores 4 and 5
        if unsafe_categories:
            summary["overall_assessment"] = (
                f"Image analysis complete. Potential unsafe content detected in categories: {', '.join(unsafe_categories)}."
            )

    return summary
