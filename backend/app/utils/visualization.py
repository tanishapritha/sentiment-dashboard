from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def sentiment_histogram(df: pd.DataFrame):
    fig = px.histogram(df, x='sentiment', color='sentiment', title='Sentiment Distribution')
    return fig.to_json()

def generate_wordcloud(df: pd.DataFrame):
    text = ' '.join(df['cleaned'].tolist())
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(15,7))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
