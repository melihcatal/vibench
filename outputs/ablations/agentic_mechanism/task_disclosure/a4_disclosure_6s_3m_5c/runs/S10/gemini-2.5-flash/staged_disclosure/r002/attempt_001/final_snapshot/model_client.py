
import os
import json
import requests

class ModelClient:
    def __init__(self, model_family: str, config_path: str = None):
        self.model_family = model_family
        self.config = self._load_config(config_path)
        self.api_key = self._get_api_key()
        self.base_url = self._get_base_url()

    def _load_config(self, config_path: str):
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "openai": {
                    "api_key_env": "OPENAI_API_KEY",
                    "base_url": "https://api.openai.com/v1/chat/completions"
                },
                "google": {
                    "api_key_env": "GOOGLE_API_KEY",
                    "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
                },
                "huggingface": {
                    "api_key_env": "HF_API_KEY",
                    "base_url": "https://api-inference.huggingface.co/models/"
                }
            }.get(self.model_family, {})

    def _get_api_key(self):
        env_var = self.config.get("api_key_env")
        if env_var:
            return os.getenv(env_var)
        return None

    def _get_base_url(self):
        return os.getenv(f"{self.model_family.upper()}_BASE_URL", self.config.get("base_url"))

    def generate_text(self, prompt: str, model_name: str = None, **kwargs):
        if not self.api_key:
            raise ValueError(f"API key for {self.model_family} not found. Please set the environment variable.")

        headers = self._get_headers()
        payload = self._build_payload(prompt, model_name, **kwargs)
        url = self._get_inference_url(model_name)

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return self._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error during API request to {self.model_family}: {e}")

    def _get_headers(self):
        if self.model_family == "openai" or self.model_family == "huggingface":
            return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        elif self.model_family == "google":
            return {"Content-Type": "application/json"}
        return {}

    def _build_payload(self, prompt: str, model_name: str, **kwargs):
        if self.model_family == "openai":
            return {
                "model": model_name or "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                **kwargs
            }
        elif self.model_family == "google":
            return {
                "contents": [{"parts": [{"text": prompt}]}],
                **kwargs
            }
        elif self.model_family == "huggingface":
            return {
                "inputs": prompt,
                **kwargs
            }
        return {"prompt": prompt, **kwargs}

    def _get_inference_url(self, model_name: str = None):
        if self.model_family == "huggingface" and model_name:
            return f"{self.base_url}{model_name}"
        return self.base_url

    def _parse_response(self, response_json):
        if self.model_family == "openai":
            return response_json.get("choices")[0].get("message").get("content")
        elif self.model_family == "google":
            return response_json.get("candidates")[0].get("content").get("parts")[0].get("text")
        elif self.model_family == "huggingface":
            return response_json[0].get("generated_text")
        return response_json
