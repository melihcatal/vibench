import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

log_message = 'User login failed due to invalid credentials'
response = openai.Moderation.create(input=log_message)
print(response['results'][0]['flagged'])
