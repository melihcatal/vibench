import openai

def moderate_text(text):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Moderation.create(input=text)
    return response['results'][0]['flagged']
