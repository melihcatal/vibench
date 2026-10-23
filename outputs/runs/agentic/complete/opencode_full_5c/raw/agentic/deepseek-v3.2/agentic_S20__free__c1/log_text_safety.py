import json
from typing import List, Dict, Any
from observability_client import get_openai_client
from observability_models import SafetyCheckResult


def check_log_safety(log_messages: List[Dict[str, Any]]) -> List[SafetyCheckResult]:
    """
    Check selected log message text for unsafe content using OpenAI Moderation API.

    Args:
        log_messages: List of log messages with 'id' and 'message' fields

    Returns:
        List of safety check results
    """
    results = []

    try:
        client = get_openai_client()

        for log in log_messages:
            log_id = log.get("id", "unknown")
            message = log.get("message", "")

            if not message:
                results.append(
                    SafetyCheckResult(
                        log_id=log_id,
                        message=message,
                        is_safe=True,
                        unsafe_categories=[],
                        confidence=1.0,
                    )
                )
                continue

            # Use OpenAI Moderation API
            response = client.moderations.create(
                model="text-moderation-latest", input=message
            )

            moderation_result = response.results[0]

            unsafe_categories = []
            for category, flagged in moderation_result.categories.model_dump().items():
                if flagged:
                    unsafe_categories.append(category)

            results.append(
                SafetyCheckResult(
                    log_id=log_id,
                    message=message[:500],  # Truncate for display
                    is_safe=not moderation_result.flagged,
                    unsafe_categories=unsafe_categories,
                    confidence=moderation_result.category_scores.get("violence", 0.0)
                    if moderation_result.flagged
                    else 1.0,
                    provider="openai",
                )
            )

    except Exception as e:
        # Fallback: simple keyword-based check
        unsafe_keywords = ["password", "secret", "key=", "token=", "credential"]

        for log in log_messages:
            log_id = log.get("id", "unknown")
            message = log.get("message", "")

            found_categories = []
            for keyword in unsafe_keywords:
                if keyword.lower() in message.lower():
                    found_categories.append(f"contains_{keyword}")

            results.append(
                SafetyCheckResult(
                    log_id=log_id,
                    message=message[:500],
                    is_safe=len(found_categories) == 0,
                    unsafe_categories=found_categories,
                    confidence=0.7 if found_categories else 0.9,
                    provider="fallback",
                )
            )

    return results


def check_single_log_safety(log_id: str, message: str) -> SafetyCheckResult:
    """
    Check a single log message for unsafe content.

    Args:
        log_id: Log identifier
        message: Log message text

    Returns:
        Safety check result
    """
    return check_log_safety([{"id": log_id, "message": message}])[0]


def filter_unsafe_logs(
    log_messages: List[Dict[str, Any]], max_confidence_threshold: float = 0.8
) -> Dict[str, List]:
    """
    Filter logs into safe and unsafe categories.

    Args:
        log_messages: List of log messages
        max_confidence_threshold: Maximum confidence score for unsafe classification

    Returns:
        Dictionary with 'safe' and 'unsafe' lists
    """
    safety_results = check_log_safety(log_messages)

    safe_logs = []
    unsafe_logs = []

    for log, result in zip(log_messages, safety_results):
        if result.is_safe and result.confidence >= max_confidence_threshold:
            safe_logs.append({"log": log, "safety_result": result.to_dict()})
        else:
            unsafe_logs.append({"log": log, "safety_result": result.to_dict()})

    return {
        "safe": safe_logs,
        "unsafe": unsafe_logs,
        "total_checked": len(log_messages),
        "unsafe_count": len(unsafe_logs),
    }


def generate_safety_report(log_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a comprehensive safety report for log messages.

    Args:
        log_messages: List of log messages

    Returns:
        Safety report dictionary
    """
    safety_results = check_log_safety(log_messages)

    # Count categories
    category_counts = {}
    for result in safety_results:
        for category in result.unsafe_categories:
            category_counts[category] = category_counts.get(category, 0) + 1

    # Calculate statistics
    total_logs = len(log_messages)
    unsafe_logs = sum(1 for r in safety_results if not r.is_safe)
    safe_logs = total_logs - unsafe_logs

    # Get most common unsafe messages
    unsafe_messages = []
    for log, result in zip(log_messages, safety_results):
        if not result.is_safe:
            unsafe_messages.append(
                {
                    "log_id": result.log_id,
                    "message_preview": result.message[:100] + "..."
                    if len(result.message) > 100
                    else result.message,
                    "categories": result.unsafe_categories,
                    "confidence": result.confidence,
                }
            )

    return {
        "summary": {
            "total_logs": total_logs,
            "safe_logs": safe_logs,
            "unsafe_logs": unsafe_logs,
            "safety_rate": safe_logs / total_logs if total_logs > 0 else 1.0,
        },
        "category_breakdown": category_counts,
        "unsafe_examples": unsafe_messages[:5],
        "provider": safety_results[0].provider if safety_results else "unknown",
    }
