import os
import requests

class ModelClient:
    def __init__(self, model_endpoint: str, api_key: str):
        if not model_endpoint:
            raise ValueError("Model endpoint cannot be empty.")
        if not api_key:
            raise ValueError("API key cannot be empty.")

        self.model_endpoint = model_endpoint
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def predict(self, data: dict) -> dict:
        """
        Sends data to the model endpoint for prediction.

        Args:
            data: A dictionary containing the input data for the model.

        Returns:
            A dictionary containing the prediction results.
        """
        try:
            response = requests.post(self.model_endpoint, headers=self.headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during prediction: {e}")
            raise

def get_model_client_from_env() -> ModelClient:
    """
    Helper function to create a ModelClient instance using environment variables.
    Expects 'MODEL_ENDPOINT' and 'MODEL_API_KEY' to be set.
    """
    model_endpoint = os.getenv("MODEL_ENDPOINT")
    api_key = os.getenv("MODEL_API_KEY")

    if not model_endpoint:
        raise EnvironmentError("MODEL_ENDPOINT environment variable not set.")
    if not api_key:
        raise EnvironmentError("MODEL_API_KEY environment variable not set.")

    return ModelClient(model_endpoint, api_key)

class SpecificModelConfig:
    DEFAULT_ENDPOINT = "https://api.example.com/v1/models/default:predict"
    DEFAULT_API_KEY_VAR = "MY_MODEL_API_KEY"

    @staticmethod
    def get_client() -> ModelClient:
        endpoint = os.getenv("SPECIFIC_MODEL_ENDPOINT", SpecificModelConfig.DEFAULT_ENDPOINT)
        api_key = os.getenv(SpecificModelConfig.DEFAULT_API_KEY_VAR)
        if not api_key:
            raise EnvironmentError(f"{SpecificModelConfig.DEFAULT_API_KEY_VAR} environment variable not set.")
        return ModelClient(endpoint, api_key)
