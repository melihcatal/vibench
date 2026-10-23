def normalize_labels(labels):
    return [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in labels]

def normalize_text_blocks(blocks):
    return [{'Text': block['Text'], 'Confidence': block['Confidence']} for block in blocks if block['BlockType'] == 'LINE']

def normalize_moderation_labels(labels):
    return [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in labels]