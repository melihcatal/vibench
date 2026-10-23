from openai import OpenAI
import os

def summarize_stored_asset_content(
    extracted_content: str
) -> str:
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'user',
                'content': f'Summarize the following extracted asset content concisely:\\n\\n{extracted_content}'
            }
        ],
        temperature=0.3,
        max_tokens=300
    )
    
    return response.choices[0].message.content
