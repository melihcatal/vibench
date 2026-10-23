import os
import requests
import json

from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse

def check_unsafe_copy(request: UnsafeContentCheckRequest) -> UnsafeContentCheckResponse:
    """Checks localized copy for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    # https://developers.perspectiveapi.com/s/docs-sample-code
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        'comment': {
            'text': request.text
        },
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        },
        'languages': [request.language]
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        analysis_result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return UnsafeContentCheckResponse(is_unsafe=False, categories_detected=[], scores={})

    is_unsafe = False
    categories_detected = []
    scores = {}

    # Threshold for considering content 'unsafe'. This can be adjusted.
    TOXICITY_THRESHOLD = 0.7

    for attribute, data in analysis_result.get('attributeScores', {}).items():
        score = data['summaryScore']['value']
        scores[attribute] = score
        if score > TOXICITY_THRESHOLD:
            is_unsafe = True
            categories_detected.append(attribute)
    
    return UnsafeContentCheckResponse(
        is_unsafe=is_unsafe,
        categories_detected=categories_detected,
        scores=scores
    )

if __name__ == '__main__':
    # Example usage for testing
    os.environ['PERSPECTIVE_API_KEY'] = 'YOUR_PERSPECTIVE_API_KEY' # Replace with your actual API key

    # Example 1: Potentially unsafe text
    req1 = UnsafeContentCheckRequest(text="You are an idiot!", language="en")
    res1 = check_unsafe_copy(req1)
    print(f"Text: \"{req1.text}\"\nIs Unsafe: {res1.is_unsafe}\nCategories: {res1.categories_detected}\nScores: {res1.scores}\n")

    # Example 2: Safe text
    req2 = UnsafeContentCheckRequest(text="Hello, how are you today?", language="en")
    res2 = check_unsafe_copy(req2)
    print(f"Text: \"{req2.text}\"\nIs Unsafe: {res2.is_unsafe}\nCategories: {res2.categories_detected}\nScores: {res2.scores}\n")

    # Example 3: Text in a different language (if supported by Perspective API for the language)
    req3 = UnsafeContentCheckRequest(text="¡Eres un imbécil!", language="es")
    res3 = check_unsafe_copy(req3)
    print(f"Text: \"{req3.text}\"\nIs Unsafe: {res3.is_unsafe}\nCategories: {res3.categories_detected}\nScores: {res3.scores}\n")
