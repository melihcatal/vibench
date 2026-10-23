import requests

from safety_client import auth_headers, endpoint_url, has_safety_credentials


def allow_text(category_scores, thresholds):
    if has_safety_credentials():
        payload = {"categoryScores": category_scores, "thresholds": thresholds}
        response = requests.post(
            endpoint_url("/contentsafety/text:threshold"),
            json=payload,
            headers=auth_headers(),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("allowed", False)
    return all(
        float(category_scores.get(k, 0.0)) < float(v) for k, v in thresholds.items()
    )
