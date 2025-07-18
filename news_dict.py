
def get_city_sites(city):
    
    return {
        "TIMES OF INDIA": {
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
        "INDIAN EXPRESS": {
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
