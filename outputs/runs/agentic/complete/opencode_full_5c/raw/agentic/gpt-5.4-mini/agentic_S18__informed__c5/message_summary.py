import json
from openai import OpenAI

def summarize_message_results(results, model='gpt-5.4-mini'):
    client = OpenAI()
    prompt = json.dumps(results, ensure_ascii=False)
    response = client.chat.completions.create(model=model, messages=[{'role':'user','content':f'Summarize these pub/sub processing results:
{prompt}'}])
    return response.choices[0].message.content
