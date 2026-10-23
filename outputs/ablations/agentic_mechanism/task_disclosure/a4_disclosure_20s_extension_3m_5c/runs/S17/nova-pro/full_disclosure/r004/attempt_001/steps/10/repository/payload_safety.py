from google.cloud import contentmoderator

def check_unsafe_content(text):
    client = contentmoderator.ImageClient()
    response = client.text_moderation(text)
    if response.is_likelihood_above(contentmoderator.Likelihood.MEDIUM):
        return True
    return False