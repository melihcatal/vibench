
class ManagedModelRequest:
    """
    Represents a request to the managed model platform.
    """
    def __init__(self, prompt: str, temperature: float = 0.7, max_tokens: int = 100):
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

    def to_platform_format(self):
        """
        Converts the local request format to the specific platform's request format.
        This is a placeholder and should be implemented based on the actual platform API.
        """
        return {
            "instances": [{"prompt": self.prompt}],
            "parameters": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            },
        }

class ManagedModelResponse:
    """
    Represents a response from the managed model platform.
    """
    def __init__(self, platform_output: dict):
        self.platform_output = platform_output
        self.generated_text = self._extract_generated_text()

    def _extract_generated_text(self):
        """
        Extracts the generated text from the platform's raw output.
        This is a placeholder and should be implemented based on the actual platform API.
        """
        if "predictions" in self.platform_output and self.platform_output["predictions"]:
            return self.platform_output["predictions"][0].get("content", "")
        return ""

    def get_text(self) -> str:
        """
        Returns the normalized generated text.
        """
        return self.generated_text

def normalize_platform_output(platform_output: dict) -> dict:
    """
    Normalizes the raw output from the managed model platform into a consistent format.
    This function can be used to standardize different platform responses.
    """
    response = ManagedModelResponse(platform_output)
    return {
        "generated_text": response.get_text(),
        "raw_platform_output": platform_output,
    }
