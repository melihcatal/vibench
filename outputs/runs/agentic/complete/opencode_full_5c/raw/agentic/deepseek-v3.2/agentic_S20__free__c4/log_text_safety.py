import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from observability_models import LogEvent


def check_log_safety(log_text: str) -> Dict[str, Any]:
    """
    Check log message text for unsafe content using Google Generative AI Safety API.

    Args:
        log_text: The log message text to check

    Returns:
        Dictionary with safety analysis results
    """
    try:
        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            return {
                "safe": True,
                "error": "GOOGLE_AI_API_KEY environment variable not set",
                "safety_categories": {},
            }

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(
            f"Analyze this log message for safety concerns: {log_text}",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
        )

        safety_ratings = {}
        if hasattr(response, "prompt_feedback") and response.prompt_feedback:
            if hasattr(response.prompt_feedback, "safety_ratings"):
                for rating in response.prompt_feedback.safety_ratings:
                    safety_ratings[rating.category.name] = {
                        "probability": rating.probability.name,
                        "blocked": rating.blocked,
                    }

        is_safe = True
        for rating in safety_ratings.values():
            if rating.get("blocked"):
                is_safe = False
                break

        return {
            "safe": is_safe,
            "log_text": log_text,
            "safety_categories": safety_ratings,
            "provider": "Google Generative AI (Gemini Pro)",
        }

    except Exception as e:
        print(f"Error checking log safety with Google AI: {e}")
        return {
            "safe": True,
            "error": str(e),
            "log_text": log_text,
            "provider": "Google Generative AI",
        }


def check_logs_safety(log_events: List[LogEvent]) -> Dict[str, Any]:
    """
    Check multiple log messages for unsafe content.

    Args:
        log_events: List of LogEvent objects

    Returns:
        Dictionary with safety analysis for all logs
    """
    results = []
    unsafe_logs = []

    for i, log_event in enumerate(log_events):
        print(f"Checking safety of log {i + 1}/{len(log_events)}...")

        result = check_log_safety(log_event.message)
        result["log_index"] = i
        result["log_level"] = (
            log_event.level.value
            if hasattr(log_event.level, "value")
            else str(log_event.level)
        )
        result["timestamp"] = (
            log_event.timestamp.isoformat() if log_event.timestamp else None
        )

        results.append(result)

        if not result.get("safe", True):
            unsafe_logs.append(
                {
                    "index": i,
                    "message": log_event.message[:100] + "..."
                    if len(log_event.message) > 100
                    else log_event.message,
                    "level": result["log_level"],
                    "safety_issues": result.get("safety_categories", {}),
                }
            )

    return {
        "total_logs": len(log_events),
        "safe_logs": len([r for r in results if r.get("safe", True)]),
        "unsafe_logs": len(unsafe_logs),
        "unsafe_log_details": unsafe_logs,
        "all_results": results,
        "provider": "Google Generative AI (Gemini Pro)",
    }


def filter_unsafe_logs(log_events: List[LogEvent]) -> List[LogEvent]:
    """
    Filter out logs with unsafe content.

    Args:
        log_events: List of LogEvent objects

    Returns:
        Filtered list of safe LogEvent objects
    """
    safe_logs = []

    for log_event in log_events:
        result = check_log_safety(log_event.message)
        if result.get("safe", True):
            safe_logs.append(log_event)
        else:
            print(f"Filtered out unsafe log: {log_event.message[:50]}...")

    return safe_logs


def analyze_log_patterns_safety(log_events: List[LogEvent]) -> Dict[str, Any]:
    """
    Analyze log patterns for safety concerns.

    Args:
        log_events: List of LogEvent objects

    Returns:
        Dictionary with pattern analysis
    """
    from collections import Counter

    messages = [log.message for log in log_events]
    message_counter = Counter(messages)

    unique_messages = list(message_counter.keys())
    safety_results = check_logs_safety(
        [LogEvent(message=msg, level="INFO") for msg in unique_messages]
    )

    unsafe_patterns = []
    for result in safety_results.get("all_results", []):
        if not result.get("safe", True):
            msg_index = result.get("log_index", 0)
            if msg_index < len(unique_messages):
                unsafe_patterns.append(
                    {
                        "message_pattern": unique_messages[msg_index],
                        "occurrences": message_counter[unique_messages[msg_index]],
                        "safety_issues": result.get("safety_categories", {}),
                    }
                )

    return {
        "total_unique_patterns": len(unique_messages),
        "unsafe_patterns": len(unsafe_patterns),
        "unsafe_pattern_details": unsafe_patterns,
        "total_log_instances": len(log_events),
        "safe_instance_percentage": (
            len(log_events) - sum(p["occurrences"] for p in unsafe_patterns)
        )
        / len(log_events)
        * 100
        if log_events
        else 100,
        "provider": "Google Generative AI (Gemini Pro)",
    }


def get_safety_recommendations(log_events: List[LogEvent]) -> List[str]:
    """
    Get safety recommendations based on log analysis.

    Args:
        log_events: List of LogEvent objects

    Returns:
        List of safety recommendations
    """
    analysis = analyze_log_patterns_safety(log_events)

    recommendations = []

    if analysis["unsafe_patterns"] > 0:
        recommendations.append(
            f"Found {analysis['unsafe_patterns']} unsafe log patterns. Review and sanitize these log messages."
        )

        for pattern in analysis["unsafe_pattern_details"][:3]:
            recommendations.append(
                f"Pattern: '{pattern['message_pattern'][:50]}...' appears {pattern['occurrences']} times"
            )

    if analysis["safe_instance_percentage"] < 95:
        recommendations.append(
            f"Only {analysis['safe_instance_percentage']:.1f}% of log instances are safe. Consider implementing log sanitization."
        )

    if not recommendations:
        recommendations.append("All log patterns appear safe. No action needed.")

    return recommendations
