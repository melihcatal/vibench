import boto3

# Set up the Amazon Comprehend client
comprehend = boto3.client('comprehend')

def moderate_claims(text):
    # Detect the sentiment of the text
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment_label = sentiment['Sentiment']
    
    # Detect entities in the text
    entities = comprehend.detect_entities(Text=text, LanguageCode='en')
    entity_list = [entity['Text'] for entity in entities['Entities']]
    
    # Detect key phrases in the text
    key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    key_phrase_list = [phrase['Text'] for phrase in key_phrases['KeyPhrases']]
    
    # Return the results
    return {
        'sentiment': sentiment_label,
        'entities': entity_list,
        'key_phrases': key_phrase_list
    }

if __name__ == '__main__':
    claim = 'The customer service was terrible and I want a refund!'
    results = moderate_claims(claim)
    print(results)