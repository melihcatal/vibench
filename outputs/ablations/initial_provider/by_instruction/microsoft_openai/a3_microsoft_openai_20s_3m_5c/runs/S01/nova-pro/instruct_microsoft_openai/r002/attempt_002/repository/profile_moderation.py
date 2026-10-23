import re

def moderate_profile_text(text):
    # Example moderation: remove profanity
    profanity_list = ['badword1', 'badword2']
    for word in profanity_list:
        text = re.sub(word, '', text)
    return text