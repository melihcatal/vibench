import os
import dashscope

# Set up the API key
os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"


# Model client utilities
def get_model_client():
    return dashscope


# Model request and response helpers
def create_model_request(text, model="qwen-turbo"):
    return {"text": text, "model": model}


def parse_model_response(response):
    return response.output.choices[0].text
