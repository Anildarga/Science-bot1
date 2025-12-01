# Science-bot1
Automated X bot for daily Sciencefacts, images and threads

# Science Bot for X/Twitter

Automated bot that posts daily science facts, NASA images, and research highlights. Built with Python + Tweepy.

## Quick Setup
1. Get X API keys: [developer.x.com](https://developer.x.com)
2. Copy .env.example to .env and fill in keys.
3. Install deps: pip install -r requirements.txt
4. Run: python science_bot.py (tests one post)
5. Deploy to Render.com for daily cron (see below).

## Deploy on Render (Free)
1. [render.com](https://render.com) → New Web Service → Connect this repo.
2. Add env vars (keys) in Render dashboard.
3. Build: pip install -r requirements.txt
4. Start: python science_bot.py
5. Add Cron: 0 12 * * * (daily at noon UTC).

Bot bio: "🤖 Automated science wonders | Powered by xAI Grok"

License: MIT
