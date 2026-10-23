from dashscope import Generation


def image_summary(image_analysis):
    response = Generation.call(
        model="qwen-vl",
        prompt=f"Summarize the following image analysis: {image_analysis}",
    )
    return response.output.text
