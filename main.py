import requests
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

TOPICS = [
    "AI", "Tech", "Business", "Finance", "Gen Z finance",
    "Crypto", "Creator Economy", "Startup Culture", "Pop Culture"
]

def fetch_headlines(query):
    response = requests.get(BASE_URL, params={
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY
    })
    try:
        response.raise_for_status()
        articles = response.json().get("articles", [])
    except:
        return []
    return [article["title"] for article in articles if article.get("title")]

def cluster_headlines(headlines, n_clusters=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(headlines)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    clustered = {i: [] for i in range(n_clusters)}
    for i, label in enumerate(labels):
        clustered[label].append(headlines[i])
    return clustered

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def summarize_cluster(headlines):
    prompt = "Summarize these headlines into one clear blog-friendly topic:\n"
    prompt += "\n".join(f"- {title}" for title in headlines)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a journalist assistant for a Gen-Z blog."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
