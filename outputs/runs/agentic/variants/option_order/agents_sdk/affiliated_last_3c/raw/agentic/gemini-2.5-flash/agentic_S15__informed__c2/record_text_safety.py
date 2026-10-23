import os
import requests

def check_text_safety(text_content: str) -> dict:
    """Checks user-generated document fields for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"status": "error", "message": "PERSPECTIVE_API_KEY environment variable not set."}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    # Perspective API endpoint hostname: commentanalyzer.googleapis.com
    
    payload = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        analysis_result = response.json()
        return {"status": "success", "analysis": analysis_result}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # Example usage:
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    #
    # text1 = "This is a wonderful product, I love it!"
    # result1 = check_text_safety(text1)
    # print("Result 1:", result1)
    #
    # text2 = "You are an idiot and I hate you!"
    # result2 = check_text_safety(text2)
    # print("Result 2:", result2)
    pass
