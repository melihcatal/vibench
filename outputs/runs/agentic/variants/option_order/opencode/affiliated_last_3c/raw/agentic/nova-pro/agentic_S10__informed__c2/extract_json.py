import os
import dashscope

# Set up the API key
os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"


# Function to extract JSON from text
def extract_json(text):
    response = dashscope.Text.extract(text=text, model="qwen-turbo")
    return response.output.choices[0].text
