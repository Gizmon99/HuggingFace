from pytrends.request import TrendReq
import datetime
from collections import defaultdict

# pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['http://72.10.160.171:15223'], retries=2, backoff_factor=0.1)
pytrends = TrendReq(hl='en-US', tz=360)
print(pytrends.trending_searches(pn="united_states"))

countries = [
    "united_states", "united_kingdom", "india", "japan", "germany",
    "canada", "france", "brazil", "australia", "china", "russia",
    "indonesia", "mexico", "south_korea", "italy", "spain",
    "saudi_arabia", "turkey", "south_africa", "nigeria"
]

trend_scores = defaultdict(int)
today = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"trends"

all_trends = []

with open(f'{filename}_countries.txt', "w", encoding="utf-8") as file:
    for country in countries:
        try:
            trending_data = pytrends.trending_searches(pn=country)
            top_10_trends = trending_data[0].tolist()[:10]
            all_trends.extend(top_10_trends)
        except Exception as e:
            print(f"Error fetching trends for {country}: {e}")
        file.write(f'{country} \n\n')
        for i, trend in enumerate(top_10_trends):
            weight = 10 - i
            trend_scores[trend] += weight
            file.write(f'{i+1} {trend} \n')
        file.write('\n')

sorted_trends = sorted(trend_scores.items(), key=lambda x: x[1], reverse=True)
top_5_trends = sorted_trends[:5]

with open(f'{filename}_all_counts.txt', "w", encoding="utf-8") as file:
    for i, (trend, score) in enumerate(sorted_trends):
        file.write(f"{i+1}. {trend} (Score: {score})\n")

with open(f'{filename}_counts.txt', "w", encoding="utf-8") as file:
    for i, (trend, score) in enumerate(top_5_trends, 1):
        file.write(f"{i}. {trend} (Score: {score})\n")

with open(f'{filename}.txt', "w", encoding="utf-8") as file:
    for i, (trend, count) in enumerate(top_5_trends, 1):
        file.write(f"{trend}\n")

print(f"Top 5 global trends of {today} saved to {filename}")
