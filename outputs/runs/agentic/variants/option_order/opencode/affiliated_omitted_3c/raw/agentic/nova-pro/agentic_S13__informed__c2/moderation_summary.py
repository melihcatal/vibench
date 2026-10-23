import os
from dashscope import TextGeneration


def summarize_moderation(decisions):
    response = TextGeneration.call(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Summarize the following moderation decisions: {decisions}",
            },
        ],
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    return response.output.choices[0].message.content
