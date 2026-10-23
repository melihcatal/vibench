import openai

def invoice_summary(invoice_data):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(engine='text-davinci-003', prompt=invoice_data, max_tokens=150)
    return response.choices[0].text.strip()