import boto3
from dashscope import Generation

def summarize_incident(logs):
    response = Generation.call(
        model='qwen-turbo',
        messages=[{'role': 'user', 'content': f'Summarize the following logs: {logs}'}]
    )
    return response.output.choices[0].message.content

if __name__ == '__main__':
    summary = summarize_incident('log1, log2, log3')
    print(summary)