from transformers import pipeline

sentiment_model = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

def analyze_sentiment(text: str) -> str:
    result = sentiment_model(text)[0]
    return result['label']
