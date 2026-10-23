from openai import OpenAI
from security_models import RotationSummaryRequest, normalize_text

client = OpenAI()
request = RotationSummaryRequest(notes='Rotate secrets monthly and verify staging labels before promotion.')
result = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'system', 'content': 'Summarize secret rotation status.'}, {'role': 'user', 'content': normalize_text(request.notes)}])
print(result.choices[0].message.content)
