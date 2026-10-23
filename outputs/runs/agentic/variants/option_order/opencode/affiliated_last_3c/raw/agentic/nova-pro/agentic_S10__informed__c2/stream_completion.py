import os
import dashscope

# Set up the API key
os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"


# Function to stream completion
def stream_completion(text):
    response = dashscope.Text.complete(text=text, model="qwen-turbo", stream=True)
    for chunk in response.output.choices[0].text:
        print(chunk, end="", flush=True)
