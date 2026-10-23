import requests
import os

def check_platform_output_safety(text: str) -> dict:
    """
    Checks platform model output for unsafe content using Azure AI Content Safety.
    
    Args:
        text: The text output from the model.
        
    Returns:
        A dictionary containing the safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    result = response.json()
    
    # Process the result to a more consumable format if needed
    safety_analysis = {
        "is_safe": True,
        "categories": {}
    }

    if "categoriesAnalysis" in result:
        for category_analysis in result["categoriesAnalysis"]:
            category = category_analysis["category"]
            severity = category_analysis["severity"]
            
            # If any category has a severity > 0, it's considered unsafe
            if severity > 0:
                safety_analysis["is_safe"] = False
            
            safety_analysis["categories"][category] = severity
            
    return safety_analysis

if __name__ == '__main__':
    # Example usage
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://your-content-safety-endpoint.cognitiveservices.azure.com/"
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = "your-azure-content-safety-key"

    # print("Checking safety for a clean text...")
    # try:
    #     clean_text = "This is a perfectly safe and positive statement."
    #     safety_report_clean = check_platform_output_safety(clean_text)
    #     print("Clean text safety report:", safety_report_clean)
    #     
    #     print("\nChecking safety for potentially unsafe text...")
    #     unsafe_text = "I hate you, you are a terrible person." # Example of a text that might trigger categories
    #     safety_report_unsafe = check_platform_output_safety(unsafe_text)
    #     print("Unsafe text safety report:", safety_report_unsafe)
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except requests.exceptions.RequestException as e:
    #     print(f"API request error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
