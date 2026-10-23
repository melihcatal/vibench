def format_moderation_result(text, analysis_result):
    """
    Formats the moderation analysis result for consistency.
    """
    categories_analysis = {}
    if analysis_result and analysis_result.categories_analysis:
        for category_a in analysis_result.categories_analysis:
            categories_analysis[category_a.category.value] = {
                "severity": category_a.severity,
                "detected": category_a.detected,
            }

    return {
        "text": text,
        "block_id": analysis_result.block_id if analysis_result else None,
        "categories_analysis": categories_analysis,
        "sexual_scores": analysis_result.sexual_scores if analysis_result else None,
        "violence_scores": analysis_result.violence_scores if analysis_result else None,
        "hate_scores": analysis_result.hate_scores if analysis_result else None,
        "self_harm_scores": analysis_result.self_harm_scores
        if analysis_result
        else None,
    }


def format_redaction_result(redacted_text):
    """
    Formats the redaction result.
    """
    return {
        "redacted_text": redacted_text,
    }
