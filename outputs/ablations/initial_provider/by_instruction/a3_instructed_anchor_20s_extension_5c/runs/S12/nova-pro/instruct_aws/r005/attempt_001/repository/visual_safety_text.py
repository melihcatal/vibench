def check_safety_text(labels):
    unsafe_texts = [label['Name'] for label in labels if label['Name'] in ['violence', 'nudity']]
    return unsafe_texts