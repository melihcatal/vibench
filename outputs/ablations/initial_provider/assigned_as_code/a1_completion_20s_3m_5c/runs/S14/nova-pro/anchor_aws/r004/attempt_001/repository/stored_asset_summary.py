import boto3
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

from storage_client import get_s3_client


def summarize_stored_asset(object_name, sentences_count=3):
    client = get_s3_client()
    response = client.get_object(Bucket='your-bucket-name', Key=object_name)
    text = response['Body'].read().decode('utf-8')
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return ' '.join(str(sentence) for sentence in summary)