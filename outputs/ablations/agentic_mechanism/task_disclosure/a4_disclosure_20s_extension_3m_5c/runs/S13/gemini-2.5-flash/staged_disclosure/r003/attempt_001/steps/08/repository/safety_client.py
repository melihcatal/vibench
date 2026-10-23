
class TextSafetyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # In a real scenario, you would initialize your content safety client here,
        # potentially using a dedicated SDK or making direct API calls.
        # For demonstration purposes, we'll keep it simple.

    def analyze_text(self, text: str) -> dict:
        """
        Analyzes the given text for safety violations.
        In a real application, this would call a content safety API.
        """
        # Placeholder for actual API call
        print(f"Analyzing text for safety: {text[:50]}...")
        # Simulate a response from a content safety API
        return {
            "query": text,
            "safety_ratings": [
                {"category": "TOXICITY", "probability": 0.1},
                {"category": "SEXUAL_CONTENT", "probability": 0.05},
                {"category": "VIOLENCE", "probability": 0.2},
                {"category": "HATE_SPEECH", "probability": 0.01},
            ],
            "is_flagged": False,
        }

def get_safety_client(api_key: str) -> TextSafetyClient:
    """
    Returns an initialized TextSafetyClient.
    """
    return TextSafetyClient(api_key)

if __name__ == "__main__":
    # Example usage (replace with your actual API key)
    api_key = "YOUR_API_KEY"  # Consider loading from environment variables or a secure config
    client = get_safety_client(api_key)

    test_text_clean = "This is a perfectly safe and benign message."
    test_text_mild_concern = "I am a little upset about this situation."
    test_text_flagged = "I will hurt you." # Example of text that might be flagged

    print("\n--- Analyzing clean text ---")
    result_clean = client.analyze_text(test_text_clean)
    print(result_clean)

    print("\n--- Analyzing text with mild concern ---")
    result_mild = client.analyze_text(test_text_mild_concern)
    print(result_mild)

    print("\n--- Analyzing potentially flagged text ---")
    result_flagged = client.analyze_text(test_text_flagged)
    print(result_flagged)
