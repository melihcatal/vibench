import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def metric_summary(metric_data):
    prompt = f'Summarize the following metric data: {metric_data}'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text