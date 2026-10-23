from dashscope import Generation

DASHSCOPE_API_KEY = "your-dashscope-api-key"


def image_summary(image_analysis_results):
    prompt = f"Summarize the following image analysis results: {image_analysis_results}"
    response = Generation.call(
        model="qwen-max", prompt=prompt, api_key=DASHSCOPE_API_KEY
    )
    return response.output.choices[0].message.content
