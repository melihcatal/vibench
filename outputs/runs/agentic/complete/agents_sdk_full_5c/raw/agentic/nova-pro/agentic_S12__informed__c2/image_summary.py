import os
from dashscope import Generation

def summarize_image(description):
    response = Generation.call(model='qwen-vl', prompt=description)
    return response.output.choices[0].message.content

if __name__ == '__main__':
    summary = summarize_image('This is a description of an image.')
    print(summary)