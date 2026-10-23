import os
from googleapiclient import discovery

def check_unsafe_content(text):
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    # You can customize the threshold for flagging content
    unsafe_attributes = {}
    for attribute, data in response['attributeScores'].items():
        if data['summaryScore']['value'] > 0.7:  # Example threshold
            unsafe_attributes[attribute] = data['summaryScore']['value']
    
    return unsafe_attributes

if __name__ == "__main__":
    script_to_check = """
    This is an example narration script. 
    It can contain various sentences, some of which might be considered offensive.
    For instance, saying "you are an idiot" could be flagged.
    """
    
    print(f"Checking script for unsafe content:\n{script_to_check}\n")
    issues = check_unsafe_content(script_to_check)
    
    if issues:
        print("Unsafe content detected:")
        for attr, score in issues.items():
            print(f"- {attr}: {score:.2f}")
    else:
        print("No unsafe content detected.")
