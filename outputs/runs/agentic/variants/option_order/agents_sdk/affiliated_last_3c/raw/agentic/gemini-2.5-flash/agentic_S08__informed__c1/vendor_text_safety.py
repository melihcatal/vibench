import os
import requests
import json

def moderate_text_safety(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + api_key

    # Request body for analysis
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {}
        }
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example Usage
    vendor_note_clean = "Thank you for your business. We appreciate your prompt payment."
    vendor_note_toxic = "This is an absolutely terrible service and I will never use it again!"
    
    if os.getenv("PERSPECTIVE_API_KEY"):
        print("Moderating clean vendor note...")
        safety_report_clean = moderate_text_safety(vendor_note_clean)
        print("Clean Note Safety Report:", json.dumps(safety_report_clean, indent=2))

        print("\nModerating potentially toxic vendor note...")
        safety_report_toxic = moderate_text_safety(vendor_note_toxic)
        print("Toxic Note Safety Report:", json.dumps(safety_report_toxic, indent=2))
    else:
        print("Please set the PERSPECTIVE_API_KEY environment variable to use Perspective API.")
