import json
import os
from google import genai

# 1. Initialize Gemini client using GitHub Secrets environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Raw incoming economic release data (Replace or hook your web scraper here)
raw_data = [
    {
        "category": "Economic growth",
        "indicator": "GDP Growth QoQ",
        "actual": "2.20%",
        "forecast": "1.50%",
        "date": "Sep 30",
    },
    {
        "category": "Inflation",
        "indicator": "CPI YoY",
        "actual": "3.7%",
        "forecast": "3.6%",
        "date": "Oct 14",
    },
    {
        "category": "Jobs market",
        "indicator": "Non-Farm Payroll",
        "actual": "29k",
        "forecast": "89k",
        "date": "Oct 02",
    },
]

# 3. Ask Gemini AI to analyze surprises and provide signals
prompt = f"""
You are a senior quantitative financial analyst. 
Analyze these economic indicators, calculate the surprise/variance, and classify each indicator as 'Bullish' or 'Bearish' for the market.
Also provide a short tactical note if relevant.

Data:
{raw_data}

Return the response strictly as a clean JSON list with keys: category, indicator, actual, forecast, surprise, signal, date, note. Do not include markdown code blocks like ```json in the output, just raw JSON.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

# Clean and parse AI response
ai_output_text = response.text.strip()
if ai_output_text.startswith("```json"):
  ai_output_text = ai_output_text[7:-3].strip()

parsed_data = json.loads(ai_output_text)

# 4. Save output to a JSON file that your website or dashboard can read
output_data = {
    "last_updated": os.environ.get("GITHUB_DATE", "Live"),
    "indicators": parsed_data,
}

with open("dashboard_data.json", "w") as f:
  json.dump(output_data, f, indent=2)

print("Successfully generated AI market analysis and updated dashboard_data.json!")
