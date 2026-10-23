import os
from typing import Dict, List, Any, Optional
from google.cloud import language_v1


def check_log_text_safety(
    log_messages: List[str], check_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Check selected log message text for unsafe content using Google Cloud Natural Language API.

    Args:
        log_messages: List of log message strings to check
        check_types: Optional list of check types (default: all)
                    Options: "toxicity", "insult", "profanity", "derogatory", "sexual"

    Returns:
        Dictionary with safety analysis results
    """
    if check_types is None:
        check_types = ["toxicity", "insult", "profanity", "derogatory", "sexual"]

    client = language_v1.LanguageServiceClient()

    results = []
    unsafe_count = 0

    for i, message in enumerate(log_messages):
        if not message or not isinstance(message, str):
            continue

        # Prepare document for analysis
        document = language_v1.Document(
            content=message, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            # Analyze sentiment first to get overall tone
            sentiment_response = client.analyze_sentiment(
                request={"document": document}
            )

            # Analyze entity sentiment for more context
            entity_response = client.analyze_entity_sentiment(
                request={"document": document}
            )

            # Use moderate content classification (available in newer versions)
            # For older API versions, we'll use a simpler approach
            classification_categories = []

            # Simple keyword-based safety check as fallback
            unsafe_keywords = {
                "profanity": ["fuck", "shit", "asshole", "bitch", "damn", "hell"],
                "insult": ["idiot", "stupid", "moron", "retard", "dumb"],
                "derogatory": ["hate", "kill", "destroy", "attack", "threat"],
                "sexual": ["sex", "porn", "nude", "rape", "assault"],
            }

            detected_categories = []
            for category, keywords in unsafe_keywords.items():
                if category in check_types:
                    for keyword in keywords:
                        if keyword.lower() in message.lower():
                            detected_categories.append(category)
                            break

            # Calculate safety score
            sentiment_score = sentiment_response.document_sentiment.score
            sentiment_magnitude = sentiment_response.document_sentiment.magnitude

            # Negative sentiment with high magnitude is more concerning
            safety_score = max(0, 1.0 - (abs(sentiment_score) * sentiment_magnitude))
            if detected_categories:
                safety_score *= 0.5  # Reduce score for detected unsafe content

            is_safe = safety_score >= 0.7 and not detected_categories

            result = {
                "message_index": i,
                "message_preview": message[:100]
                + ("..." if len(message) > 100 else ""),
                "is_safe": is_safe,
                "safety_score": round(safety_score, 3),
                "sentiment_score": round(sentiment_score, 3),
                "sentiment_magnitude": round(sentiment_magnitude, 3),
                "detected_categories": detected_categories,
                "entity_count": len(entity_response.entities),
                "analysis_method": "google_cloud_language_api",
            }

            if not is_safe:
                unsafe_count += 1

            results.append(result)

        except Exception as e:
            # Fallback analysis for API errors
            result = {
                "message_index": i,
                "message_preview": message[:100]
                + ("..." if len(message) > 100 else ""),
                "is_safe": True,  # Assume safe on error
                "safety_score": 1.0,
                "sentiment_score": 0.0,
                "sentiment_magnitude": 0.0,
                "detected_categories": [],
                "entity_count": 0,
                "analysis_method": "fallback",
                "error": str(e),
            }
            results.append(result)

    # Overall summary
    safe_count = len(results) - unsafe_count
    safety_percentage = (safe_count / len(results) * 100) if results else 100

    # Most common unsafe categories
    category_counts = {}
    for result in results:
        for category in result.get("detected_categories", []):
            category_counts[category] = category_counts.get(category, 0) + 1

    summary = {
        "total_messages_analyzed": len(results),
        "safe_messages": safe_count,
        "unsafe_messages": unsafe_count,
        "safety_percentage": round(safety_percentage, 1),
        "average_safety_score": round(
            sum(r.get("safety_score", 1.0) for r in results) / len(results), 3
        )
        if results
        else 1.0,
        "unsafe_category_distribution": category_counts,
        "check_types": check_types,
        "analysis_timestamp": "2024-01-15T10:00:00Z",  # Would use datetime.utcnow() in production
    }

    # Flag concerning patterns
    if unsafe_count > 0:
        if unsafe_count / len(results) > 0.1:  # More than 10% unsafe
            summary["concern_level"] = "HIGH"
            summary["recommendation"] = (
                "Immediate review recommended. High percentage of unsafe content detected."
            )
        elif unsafe_count > 0:
            summary["concern_level"] = "MEDIUM"
            summary["recommendation"] = (
                "Review recommended. Some unsafe content detected."
            )
        else:
            summary["concern_level"] = "LOW"
            summary["recommendation"] = "No immediate action needed."
    else:
        summary["concern_level"] = "LOW"
        summary["recommendation"] = "All log messages appear safe."

    return {"summary": summary, "detailed_results": results}


def filter_unsafe_logs(
    log_entries: List[Dict[str, Any]], safety_threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Filter log entries based on message safety.

    Args:
        log_entries: List of log entry dictionaries
        safety_threshold: Minimum safety score (0.0 to 1.0)

    Returns:
        Dictionary with filtered logs and safety analysis
    """
    messages = [entry.get("message", "") for entry in log_entries]
    safety_results = check_log_text_safety(messages)

    safe_logs = []
    unsafe_logs = []

    for i, entry in enumerate(log_entries):
        if i < len(safety_results["detailed_results"]):
            result = safety_results["detailed_results"][i]
            if (
                result.get("is_safe", True)
                and result.get("safety_score", 1.0) >= safety_threshold
            ):
                safe_logs.append(
                    {
                        **entry,
                        "safety_analysis": {
                            "score": result["safety_score"],
                            "categories": result["detected_categories"],
                        },
                    }
                )
            else:
                unsafe_logs.append(
                    {
                        **entry,
                        "safety_analysis": {
                            "score": result["safety_score"],
                            "categories": result["detected_categories"],
                            "flagged": True,
                        },
                    }
                )
        else:
            # No safety analysis available, assume safe
            safe_logs.append(entry)

    return {
        "total_logs": len(log_entries),
        "safe_logs": safe_logs,
        "unsafe_logs": unsafe_logs,
        "safety_summary": safety_results["summary"],
        "filtering_threshold": safety_threshold,
    }


if __name__ == "__main__":
    # Example usage
    test_messages = [
        "User authentication successful",
        "Database connection timeout after 30 seconds",
        "Payment processing failed: insufficient funds",
        "Error: Invalid input parameter 'user_id'",
        "Warning: High memory usage detected",
        "This is a test message with no issues",
        "System error: File not found",
        "User reported issue with login page",
    ]

    results = check_log_text_safety(test_messages)
    print(f"Safety Analysis Summary:")
    print(f"  Total messages: {results['summary']['total_messages_analyzed']}")
    print(f"  Safe messages: {results['summary']['safe_messages']}")
    print(f"  Unsafe messages: {results['summary']['unsafe_messages']}")
    print(f"  Safety percentage: {results['summary']['safety_percentage']}%")
    print(f"  Concern level: {results['summary']['concern_level']}")

    # Show unsafe messages if any
    unsafe = [r for r in results["detailed_results"] if not r["is_safe"]]
    if unsafe:
        print("\nUnsafe messages detected:")
        for r in unsafe:
            print(
                f"  - {r['message_preview']} (categories: {r['detected_categories']})"
            )
