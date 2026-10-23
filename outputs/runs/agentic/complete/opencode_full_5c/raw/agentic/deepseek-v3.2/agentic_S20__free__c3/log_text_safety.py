import json
from typing import Dict, Any, List, Optional
from google.cloud import language_v1
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogEntry


def check_log_safety(log_message: str, check_types: List[str] = None) -> Dict[str, Any]:
    if check_types is None:
        check_types = ["toxicity", "insult", "profanity", "threat"]

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=log_message, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
    )

    try:
        response = client.analyze_sentiment(request={"document": document})

        safety_analysis = {
            "text": log_message[:200] + "..."
            if len(log_message) > 200
            else log_message,
            "sentiment_score": response.document_sentiment.score,
            "sentiment_magnitude": response.document_sentiment.magnitude,
            "safety_checks": {},
        }

        if "toxicity" in check_types:
            safety_analysis["safety_checks"]["toxicity"] = analyze_toxicity_patterns(
                log_message
            )

        if "insult" in check_types:
            safety_analysis["safety_checks"]["insult"] = check_for_insults(log_message)

        if "profanity" in check_types:
            safety_analysis["safety_checks"]["profanity"] = check_for_profanity(
                log_message
            )

        if "threat" in check_types:
            safety_analysis["safety_checks"]["threat"] = check_for_threats(log_message)

        safety_analysis["overall_safe"] = all(
            not check.get("found", False)
            for check in safety_analysis["safety_checks"].values()
            if isinstance(check, dict)
        )

        return safety_analysis
    except Exception as e:
        return {
            "text": log_message[:200] + "..."
            if len(log_message) > 200
            else log_message,
            "error": str(e),
            "safety_checks": {},
            "overall_safe": True,
        }


def analyze_toxicity_patterns(text: str) -> Dict[str, Any]:
    toxic_keywords = [
        "hate",
        "racist",
        "sexist",
        "discriminat",
        "bigot",
        "prejudice",
        "offensive",
        "derogatory",
        "slur",
        "abusive",
        "harass",
    ]

    found_keywords = []
    text_lower = text.lower()

    for keyword in toxic_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)

    return {
        "found": len(found_keywords) > 0,
        "keywords_found": found_keywords,
        "confidence": min(len(found_keywords) * 0.3, 1.0),
    }


def check_for_insults(text: str) -> Dict[str, Any]:
    insult_patterns = [
        "stupid",
        "idiot",
        "moron",
        "dumb",
        "fool",
        "incompetent",
        "worthless",
        "useless",
        "pathetic",
        "ridiculous",
        "nonsense",
    ]

    found_insults = []
    text_lower = text.lower()

    for insult in insult_patterns:
        if insult in text_lower:
            found_insults.append(insult)

    return {
        "found": len(found_insults) > 0,
        "insults_found": found_insults,
        "confidence": min(len(found_insults) * 0.25, 1.0),
    }


def check_for_profanity(text: str) -> Dict[str, Any]:
    profanity_list = [
        "fuck",
        "shit",
        "ass",
        "damn",
        "hell",
        "bitch",
        "crap",
        "piss",
        "dick",
        "cock",
        "pussy",
        "bastard",
        "whore",
    ]

    found_profanity = []
    text_lower = text.lower()

    for word in profanity_list:
        if word in text_lower:
            found_profanity.append(word)

    return {
        "found": len(found_profanity) > 0,
        "profanity_found": found_profanity,
        "confidence": min(len(found_profanity) * 0.4, 1.0),
    }


def check_for_threats(text: str) -> Dict[str, Any]:
    threat_patterns = [
        "kill",
        "murder",
        "attack",
        "destroy",
        "harm",
        "hurt",
        "threat",
        "danger",
        "violence",
        "weapon",
        "bomb",
        "shoot",
    ]

    found_threats = []
    text_lower = text.lower()

    for threat in threat_patterns:
        if threat in text_lower:
            found_threats.append(threat)

    return {
        "found": len(found_threats) > 0,
        "threats_found": found_threats,
        "confidence": min(len(found_threats) * 0.35, 1.0),
    }


def scan_recent_logs_for_safety(
    minutes_ago: int = 60, limit: int = 50
) -> Dict[str, Any]:
    logs_response = fetch_recent_logs(minutes_ago=minutes_ago, limit=limit)

    unsafe_logs = []
    total_checked = 0

    for event in logs_response.events:
        try:
            log_data = json.loads(event.get("message", ""))
            log_message = log_data.get("message", "")

            if log_message:
                safety_result = check_log_safety(log_message)

                if not safety_result.get("overall_safe", True):
                    unsafe_logs.append(
                        {
                            "timestamp": event.get("timestamp"),
                            "log_message": log_message[:100] + "..."
                            if len(log_message) > 100
                            else log_message,
                            "safety_issues": safety_result.get("safety_checks", {}),
                            "service": log_data.get("service", "unknown"),
                        }
                    )

                total_checked += 1
        except:
            continue

    return {
        "total_logs_checked": total_checked,
        "unsafe_logs_found": len(unsafe_logs),
        "unsafe_logs": unsafe_logs[:10],
        "time_range": f"Last {minutes_ago} minutes",
        "scan_completed": True,
    }


def check_log_entry_safety(log_entry: LogEntry) -> Dict[str, Any]:
    safety_result = check_log_safety(log_entry.message)

    return {
        "log_entry": {
            "timestamp": log_entry.timestamp,
            "service": log_entry.service,
            "component": log_entry.component,
            "message_preview": log_entry.message[:150] + "..."
            if len(log_entry.message) > 150
            else log_entry.message,
        },
        "safety_analysis": safety_result,
        "requires_review": not safety_result.get("overall_safe", True),
    }


if __name__ == "__main__":
    test_message = "User reported offensive content in the system. The message contained inappropriate language."
    safety = check_log_safety(test_message)
    print(f"Safety check: {json.dumps(safety, indent=2)}")

    recent_safety_scan = scan_recent_logs_for_safety(minutes_ago=30, limit=20)
    print(f"\nRecent logs safety scan: {json.dumps(recent_safety_scan, indent=2)}")
