import requests
from bs4 import BeautifulSoup
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

st.title("City News with Sentiment Scores")
city = st.text_input("Enter city name:", "delhi").strip().lower()
news_amt = st.slider("Articles Quantity:", 1, 20, 5)


citySites = {
    "TOI": {
        "url": f"https://timesofindia.indiatimes.com/city/{city}",
        "article_selector": "a",
        "filter": lambda href: "articleshow" in href,
        "base_url": "https://timesofindia.indiatimes.com"
    },
    "NDTV": {
        "url": f"https://www.ndtv.com/{city}-news#pfrom=home-ndtv_mainnavigation",
        "article_selector": "a",
        "filter": lambda href: f"{city}-news" in href,
        "base_url": "https://www.ndtv.com"
    },
    "INDEXP": {
        "url": f"https://indianexpress.com/section/cities/{city}/",
        "article_selector": "a",
        "filter": lambda href: f"article/cities/" in href,
        "base_url": "https://indianexpress.com"
    },"TRIBUNE": {
        "url": f"https://www.tribuneindia.com/news/city/{city}",
        "article_selector": "a",
        "filter": lambda href: f"/news/{city}/" in href,
        "base_url": "https://www.tribuneindia.com"
    }
}

def fetch_news(data):
    try:
        response = requests.get(data["url"])
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for tag in soup.find_all(data["article_selector"], href=True):
            href = tag["href"]
            title = tag.text.strip()
            if data["filter"](href) and len(title.split()) > 10:
                full_link = href if href.startswith("http") else data["base_url"] + href
                articles.append((title, full_link))

        return articles[:news_amt]  
    except Exception as e:
        return [(f"Error scraping: {e}", "")]

def shorten_text(text, max_length=20):
    if len(text.split()) > max_length:
        return ' '.join(text.split()[:max_length]) + '...'
    return text

def sentiment_label(score):
    if score >= 0.05:
        return "😊 Positive"
    elif score <= -0.05:
        return "😡 Negative"
    else:
        return "😐 Neutral"


if city:
    for name, data in citySites.items():    
        st.subheader(f"{name}")
        articles = fetch_news(data)
        cols = st.columns(3)

        for i, (title, link) in enumerate(articles):
            with cols[i%3]:
                with st.container(border=True):
                    score = analyzer.polarity_scores(title)['compound']
                    label = sentiment_label(score)
                    title = shorten_text(title, 10)

                    card_height = 200  

                    st.markdown(
                        f"""
                        <div style='height: {card_height}px; overflow: hidden;'>
                            <p style='font-weight: bold; font-size: 16px'>{title}</p>
                            <p><a href='{link}' target='_blank'>Read more</a></p>
                            <p>Sentiment: {label}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
           
