import os
from typing import Optional

class SafetyClientConfig:
    """Configuration for text content safety clients."""
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, region: Optional[str] = None):
        self.api_key = api_key
        self.endpoint = endpoint
        self.region = region

    @classmethod
    def from_env(cls, prefix: str):
        """Loads configuration from environment variables with a given prefix."""
        api_key = os.environ.get(f"{prefix}_API_KEY")
        endpoint = os.environ.get(f"{prefix}_ENDPOINT")
        region = os.environ.get(f"{prefix}_REGION")
        return cls(api_key=api_key, endpoint=endpoint, region=region)

class GenericSafetyClient:
    """A placeholder for a generic safety client."""
    def __init__(self, config: SafetyClientConfig):
        self.config = config

    def analyze_text(self, text: str) -> dict:
        """Simulates text analysis."""
        print(f"Analyzing text with generic client (endpoint: {self.config.endpoint}): '{text}'")
        return {"status": "simulated_success", "text": text}

# Example usage (not part of the tool execution, for illustration)
# if __name__ == "__main__":
#     os.environ["EXAMPLE_API_KEY"] = "sk-example"
#     os.environ["EXAMPLE_ENDPOINT"] = "https://example.com/api"
#     config = SafetyClientConfig.from_env("EXAMPLE")
#     client = GenericSafetyClient(config)
#     result = client.analyze_text("Hello world!")
#     print(result)
