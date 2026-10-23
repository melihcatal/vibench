import boto3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    frequency_dist = nltk.FreqDist(filtered_tokens)
    most_common_words = frequency_dist.most_common(5)
    summary = ' '.join([word for word, freq in most_common_words])
    return summary