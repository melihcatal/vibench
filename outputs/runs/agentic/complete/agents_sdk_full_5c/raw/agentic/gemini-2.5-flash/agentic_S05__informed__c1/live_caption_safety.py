import os
import requests
import json

def check_content_safety(text: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    body = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        
        safety_analysis = {}
        for category_result in result.get("categoriesAnalysis", []):
            category = category_result["category"]
            severity = category_result["severity"]
            if severity > 0:
                safety_analysis[category] = severity
        
        if safety_analysis:
            print(f"Content Safety Warning for text: '{text}' - {safety_analysis}")
            return safety_analysis
        else:
            print(f"Content is safe: '{text}'")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during content safety check: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}

# Example usage (for integration test):
# if __name__ == "__main__":
#     os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
#     os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"
#     check_content_safety("I hate you, you are so stupid.")
#     check_content_safety("This is a perfectly safe sentence.")
