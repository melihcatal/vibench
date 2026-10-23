import os
from tisane import TisaneClient

# Configure Tisane credentials via env variable
os.environ["TISANE_API_KEY"] = "your-tisane-key"


class ContentSafetyChecker:
    def __init__(self):
        self.client = TisaneClient()

    def check_content(self, text: str) -> dict:
        """Check the extracted text for unsafe or toxic content."""
        # Simple moderation call; adjust parameters as required by Tisane
        result = self.client.moderate(text)
        return result


def main():
    checker = ContentSafetyChecker()
    # Example usage with dummy text
    text = "I don't think this should be published."
    safety_result = checker.check_content(text)
    print("Content safety result:", safety_result)


if __name__ == "__main__":
    main()
