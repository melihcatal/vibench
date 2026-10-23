import os
import dashscope

# Set up the API key
os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"


# Function to summarize text
def summarize_text(text):
    response = dashscope.Text.summarize(text=text, model="qwen-turbo")
    return response.output.choices[0].text
