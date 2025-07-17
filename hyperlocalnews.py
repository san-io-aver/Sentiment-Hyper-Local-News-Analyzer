import requests
from bs4 import BeautifulSoup
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setup VADER
analyzer = SentimentIntensityAnalyzer()

# Get user input
city = st.text_input("Enter city name:", "delhi").strip().lower()

# Define news sources
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
    }
}

# Function to scrape articles
def fetch_news(data):
    try:
        response = requests.get(data["url"])
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for tag in soup.find_all(data["article_selector"], href=True):
            href = tag["href"]
            title = tag.text.strip()
            if data["filter"](href) and len(title.split()) > 3:
                full_link = href if href.startswith("http") else data["base_url"] + href
                articles.append((title, full_link))

        return articles[:10]  # Return top 10
    except Exception as e:
        return [(f"Error scraping: {e}", "")]

# Sentiment Emoji Map
def sentiment_label(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

st.title("City News with Sentiment")

if city:
    for name, data in citySites.items():
        st.header(f"📡 {name}")
        articles = fetch_news(data)
        for title, link in articles:
            score = analyzer.polarity_scores(title)['compound']
            label = sentiment_label(score)
            st.markdown(f"** [{title}]({link})**")
            st.write(f"Sentiment: {label}")
