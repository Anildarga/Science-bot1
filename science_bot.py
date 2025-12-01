import tweepy
import requests
import random
import datetime
import os
import io
from dotenv import load_dotenv

load_dotenv()

# === YOUR KEYS (from .env) ===
BEARER = os.getenv("BEARER")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with X API
client = tweepy.Client(
    bearer_token=BEARER,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Free image sources (get Unsplash key at unsplash.com/developers - free)
unsplash_key = os.getenv("UNSPLASH_KEY", "YOUR_UNSPLASH_ACCESS_KEY")  # Optional
nasa_apod = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"  # Works without key for demo

science_facts = [
    "A teaspoon of neutron star would weigh about 110 million tons.",
    "Octopuses have three hearts and blue blood (copper-based hemocyanin).",
    "The universe is expanding faster than ever — and we still don’t know why.",
    "Quantum entanglement allows particles to influence each other instantly, regardless of distance.",
    "Your body replaces 330 billion cells every day — that's like a new you every few months!",
    # Add more or generate with AI below
]

def get_apod():
    try:
        r = requests.get(nasa_apod).json()
        return r["url"], r["title"]
    except:
        return None, None

def get_unsplash(query="space"):
    if not unsplash_key or unsplash_key == "YOUR_UNSPLASH_ACCESS_KEY":
        return None
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={unsplash_key}"
    try:
        return requests.get(url).json()["urls"]["regular"]
    except:
        return None

def daily_fact():
    today = datetime.date.today()
    facts = {
        "12-17": "1903 — Wright brothers’ first powered flight (12 seconds, 36 meters).",
        "07-20": "1969 — Neil Armstrong became the first human on the Moon.",
        "10-04": "1957 — Sputnik 1, humanity’s first artificial satellite, launched.",
        "04-12": "1961 — Yuri Gagarin becomes the first human in space.",
    }
    month_day = today.strftime("%m-%d")
    return facts.get(month_day, random.choice(science_facts))

def post_science():
    fact = daily_fact()
    
    choice = random.random()
    if choice < 0.5 and unsplash_key != "YOUR_UNSPLASH_ACCESS_KEY":
        img_url = get_unsplash(random.choice(["space", "microscope", "physics", "chemistry", "nebula", "brain", "dna"]))
        caption = f"✨ {fact}\n\n#Science #Space #DailyFact"
        media_url = img_url
    elif choice < 0.8:
        url, title = get_apod()
        if url:
            caption = f"Astronomy Picture of the Day\n{title}\n\n{url}\n#APOD #NASA"
            media_url = url
        else:
            caption = f"{fact}\n#Science"
            media_url = None
    else:
        caption = f"New breakthrough: Room-temperature superconductors get closer with twisted graphene layers. (Nature, Dec 2025)\n\n#Research #Physics"
        media_url = None

    try:
        if media_url:
            img_data = requests.get(media_url).content
            media = client.media_upload(filename="science_img.jpg", file=io.BytesIO(img_data))
            response = client.create_tweet(text=caption, media_ids=[media.media_id])
        else:
            response = client.create_tweet(text=caption)
        print(f"Posted at {datetime.datetime.now()}: {caption[:60]}... Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Error posting: {e}")

# Optional: AI Fact Generator (add OpenAI key to .env as OPENAI_API_KEY)
# Uncomment and import openai if using
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
# def ai_fact():
#     prompt = "Write ONE engaging science fact (max 200 chars) with emoji and #hashtags."
#     resp = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=100)
#     return resp.choices[0].message.content

if _name_ == "_main_":
    post_science()
