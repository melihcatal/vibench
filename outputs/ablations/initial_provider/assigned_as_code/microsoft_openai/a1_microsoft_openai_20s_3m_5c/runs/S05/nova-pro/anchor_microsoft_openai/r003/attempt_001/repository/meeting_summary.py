import requests

def summarize_meeting(transcript):
    url = f'https://api.meaningcloud.com/summarization-1.0?key={os.getenv('MEANINGCLOUD_API_KEY')}'
    data = {
        'txt': transcript,
        'sentences': 5
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['summary']