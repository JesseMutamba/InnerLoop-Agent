# Inner Loop Trend Agent

AI-powered trend detection system built for smart media coverage across Gen Z culture, finance, and tech.

## Features
- Fetches real-time headlines from NewsAPI
- Clusters stories into trending topics
- ✍Uses GPT to generate blog-ready summaries
- Sends daily email briefs
- Clean Streamlit dashboard

## Setup

1. Clone the repo
2. Create `.env` file using `.env.example`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the dashboard:
   ```
   streamlit run app.py
   ```

5. Start daily email runner (optional):
   ```
   python daily_email_runner.py
   ```

## License
MIT
