import requests

def stream_platform_generation():
    url = 'https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-6b-beta'
    headers = {'Authorization': 'Bearer YOUR_HUGGINGFACE_TOKEN'}
    response = requests.post(url, headers=headers, stream=True)
    return response