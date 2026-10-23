import os
import requests
import json


def check_text_safety(text, languages=["en"]):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": text},
        "languages": languages,
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
    }

    params = {"key": api_key}

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        scores = {}
        for attribute_name, attribute_data in result.get("attributeScores", {}).items():
            scores[attribute_name] = attribute_data.get("summaryScore", {}).get(
                "value", 0
            )

        return {
            "is_safe": all(score < 0.7 for score in scores.values()),
            "scores": scores,
            "flagged_attributes": [
                attr for attr, score in scores.items() if score >= 0.7
            ],
            "highest_score": max(scores.values()) if scores else 0,
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Perspective API request failed: {str(e)}")


def check_narration_script_safety(script_text):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": script_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "doNotStore": True,
    }

    params = {"key": api_key}

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        safety_result = {
            "script": script_text,
            "scores": {},
            "recommendation": "safe",
            "warnings": [],
        }

        threshold = 0.7
        warning_threshold = 0.5

        for attribute_name, attribute_data in result.get("attributeScores", {}).items():
            score = attribute_data.get("summaryScore", {}).get("value", 0)
            safety_result["scores"][attribute_name] = score

            if score >= threshold:
                safety_result["recommendation"] = "unsafe"
                safety_result["warnings"].append(
                    f"High {attribute_name.lower().replace('_', ' ')} score: {score:.2f}"
                )
            elif score >= warning_threshold:
                safety_result["warnings"].append(
                    f"Moderate {attribute_name.lower().replace('_', ' ')} score: {score:.2f}"
                )

        return safety_result
    except requests.exceptions.RequestException as e:
        raise Exception(f"Perspective API request failed: {str(e)}")


def batch_check_safety(scripts):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}

    results = []

    for script in scripts:
        payload = {
            "comment": {"text": script},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "doNotStore": True,
        }

        try:
            response = requests.post(url, params=params, json=payload)
            response.raise_for_status()

            result = response.json()

            scores = {}
            for attribute_name, attribute_data in result.get(
                "attributeScores", {}
            ).items():
                scores[attribute_name] = attribute_data.get("summaryScore", {}).get(
                    "value", 0
                )

            results.append(
                {
                    "script": script,
                    "is_safe": all(score < 0.7 for score in scores.values()),
                    "scores": scores,
                    "highest_score": max(scores.values()) if scores else 0,
                }
            )
        except requests.exceptions.RequestException as e:
            results.append({"script": script, "error": str(e), "is_safe": False})

    return results


def get_safety_thresholds():
    return {"safe": 0.3, "warning": 0.5, "unsafe": 0.7, "severe": 0.9}


def filter_unsafe_scripts(scripts, threshold=0.7):
    safety_results = batch_check_safety(scripts)

    safe_scripts = []
    unsafe_scripts = []

    for result in safety_results:
        if result.get("is_safe", False):
            safe_scripts.append(result["script"])
        else:
            unsafe_scripts.append(
                {
                    "script": result["script"],
                    "highest_score": result.get("highest_score", 0),
                    "scores": result.get("scores", {}),
                }
            )

    return {
        "safe": safe_scripts,
        "unsafe": unsafe_scripts,
        "total_checked": len(scripts),
        "safe_count": len(safe_scripts),
        "unsafe_count": len(unsafe_scripts),
    }
