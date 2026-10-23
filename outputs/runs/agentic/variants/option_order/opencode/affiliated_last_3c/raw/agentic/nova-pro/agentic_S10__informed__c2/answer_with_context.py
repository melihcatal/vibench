import os
import dashscope

# Set up the API key
os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"


# Function to answer a question with context
def answer_with_context(question, context):
    response = dashscope.Text.answer(
        question=question, context=context, model="qwen-turbo"
    )
    return response.output.choices[0].text
