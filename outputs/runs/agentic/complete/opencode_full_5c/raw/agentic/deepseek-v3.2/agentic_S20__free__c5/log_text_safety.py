import os
import json
from typing import List, Dict, Any
from observability_models import LogSafetyCheck


def check_log_safety(
    log_messages: List[str], categories: List[str] = None
) -> List[LogSafetyCheck]:
    """
    Check selected log message text for unsafe content using Google Cloud Perspective API.

    Args:
        log_messages: List of log messages to check
        categories: Specific safety categories to check (default: all)

    Returns:
        List of LogSafetyCheck objects with safety analysis results
    """
    try:
        from googleapiclient import discovery
        from google.oauth2 import service_account

        if categories is None:
            categories = [
                "TOXICITY",
                "SEVERE_TOXICITY",
                "IDENTITY_ATTACK",
                "INSULT",
                "PROFANITY",
                "THREAT",
                "SEXUALLY_EXPLICIT",
            ]

        credentials_info = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if credentials_info:
            credentials_dict = json.loads(credentials_info)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
        else:
            credentials = None

        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            credentials=credentials,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

        results = []

        for message in log_messages:
            if not message or len(message.strip()) == 0:
                results.append(
                    LogSafetyCheck(
                        message=message,
                        is_safe=True,
                        unsafe_categories=[],
                        confidence=1.0,
                        provider="google_perspective",
                    )
                )
                continue

            analyze_request = {
                "comment": {"text": message},
                "requestedAttributes": {category: {} for category in categories},
                "languages": ["en"],
            }

            try:
                response = client.comments().analyze(body=analyze_request).execute()

                unsafe_categories = []
                max_score = 0.0

                for category in categories:
                    if category in response.get("attributeScores", {}):
                        score = response["attributeScores"][category]["summaryScore"][
                            "value"
                        ]
                        if score > 0.7:
                            unsafe_categories.append(category)
                            if score > max_score:
                                max_score = score

                is_safe = len(unsafe_categories) == 0
                confidence = 1.0 - max_score if not is_safe else 1.0

                results.append(
                    LogSafetyCheck(
                        message=message,
                        is_safe=is_safe,
                        unsafe_categories=unsafe_categories,
                        confidence=confidence,
                        provider="google_perspective",
                    )
                )

            except Exception as e:
                print(f"Error analyzing message with Perspective API: {e}")
                results.append(
                    LogSafetyCheck(
                        message=message,
                        is_safe=True,
                        unsafe_categories=[],
                        confidence=0.0,
                        provider="google_perspective",
                    )
                )

        unsafe_count = sum(1 for result in results if not result.is_safe)
        print(f"Safety check completed using Google Cloud Perspective API")
        print(
            f"Checked {len(results)} messages, found {unsafe_count} potentially unsafe"
        )

        return results

    except Exception as e:
        print(f"Failed to check log safety with Google Cloud Perspective API: {e}")

        fallback_results = []
        for message in log_messages:
            fallback_results.append(
                LogSafetyCheck(
                    message=message,
                    is_safe=True,
                    unsafe_categories=[],
                    confidence=1.0,
                    provider="fallback",
                )
            )

        return fallback_results
