from profanity_check import predict

def check_safety_text(text):
    safety_score = predict([text])
    return safety_score[0] == 0