from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def sentiment_histogram(df: pd.DataFrame):
    fig = px.histogram(df, x='sentiment', color='sentiment', title='Sentiment Distribution')
    return fig.to_json()

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

def generate_wordcloud(df: pd.DataFrame):
    text = " ".join(df["cleaned"].tolist())
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Save to BytesIO instead of plt.show()
    img_io = BytesIO()
    plt.figure(figsize=(15, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(img_io, format="png", bbox_inches="tight")
    plt.close()
    img_io.seek(0)

    # Encode image to base64 for frontend
    img_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")
    return {"wordcloud": img_base64}

