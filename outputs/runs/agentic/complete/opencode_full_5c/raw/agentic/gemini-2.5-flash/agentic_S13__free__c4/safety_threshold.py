import os
from typing import Dict
from google.cloud import logging  # Provider identifiable import


def apply_safety_thresholds(
    moderation_scores: Dict[str, float], thresholds: Dict[str, float], project_id: str
) -> bool:
    """Applies category thresholds to decide whether to allow text and logs the decision.

    Args:
        moderation_scores: A dictionary of moderation categories and their scores.
        thresholds: A dictionary of category names and their corresponding score thresholds.
        project_id: The Google Cloud project ID.

    Returns:
        True if the text is allowed based on thresholds, False otherwise.
    """
    logging_client = logging.Client(project=project_id)
    logger = logging_client.logger("safety_threshold_decisions")

    decision_allowed = True
    reasons_for_denial = []

    for category, score in moderation_scores.items():
        if category in thresholds and score > thresholds[category]:
            decision_allowed = False
            reasons_for_denial.append(
                f"{category} (score: {score:.2f} > threshold: {thresholds[category]:.2f})"
            )

    if decision_allowed:
        log_message = "Text allowed by safety thresholds."
        logger.log_text(log_message, severity="INFO", labels={"decision": "allowed"})
    else:
        log_message = f"Text denied by safety thresholds. Reasons: {'; '.join(reasons_for_denial)}"
        logger.log_text(log_message, severity="WARNING", labels={"decision": "denied"})

    return decision_allowed


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        # Example usage
        mock_scores_unsafe = {"Toxicity": 0.9, "Sexual": 0.1, "Threat": 0.7}
        mock_scores_safe = {"Toxicity": 0.05, "Sexual": 0.02, "Threat": 0.01}
        custom_thresholds = {"Toxicity": 0.8, "Threat": 0.5}

        allowed_unsafe = apply_safety_thresholds(
            mock_scores_unsafe, custom_thresholds, project_id
        )
        print(f"Unsafe text allowed: {allowed_unsafe}")

        allowed_safe = apply_safety_thresholds(
            mock_scores_safe, custom_thresholds, project_id
        )
        print(f"Safe text allowed: {allowed_safe}")
