from openai import AzureOpenAI



def collect_platform_metadata(response):
    return {
        'text': response.choices[0].message.content,
        'usage': response.usage,
        'model': response.model,
        'id': response.id
    }