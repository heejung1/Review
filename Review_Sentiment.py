import requests
import json
import pandas as pd
import sys

df = pd.read_csv('Nam_reviews_kakao.csv', encoding='utf-8-sig')

import re

#전처리
def preprocess_text(text):
     text = re.sub(r'[^가-힣 ]', '', str(text), re.UNICODE)
     text = re.sub(r'\b더보기\b', '', str(text))
     text = re.sub('\s+', ' ', text).strip()
     return text


df['리뷰'] = df['리뷰'].apply(preprocess_text)
df = df[df['리뷰'] != '']

# 중복 제거
df = df.drop_duplicates(subset=['리뷰'], keep='first')

review_text = df['리뷰']

client_id = "8z47hfo7sw"
client_secret = "OFnp7HqkiGS0WyuxjF1Fli3LGKzdnnIVquIYhNb4"

url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
headers={   "X-NCP-APIGW-API-KEY-ID": client_id, 
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/json"}

sentiment = []
negative = []
positive = []
neutral = []

for i in review_text:
    content = i
    data  = {
        "content": content
    }

    response = requests.post(url,headers=headers, data=json.dumps(data) )
    rescode = response.status_code

    if rescode == 200:
        parsed_data = response.json()

        senti = parsed_data['document']['sentiment']
        sentiment.append(senti)

        confidence = parsed_data['document']['confidence']
        negative.append(confidence['negative'])
        positive.append(confidence['positive'])
        neutral.append(confidence['neutral'])
    else:
        print("Error:", response.text)

data = {
    'review': review_text,
    'sentiment': sentiment,
    'negative': negative,
    'positive': positive,
    'neutral': neutral
}
result_df = pd.DataFrame(data)
print(result_df)

negative_reviews = result_df[result_df['sentiment'] == 'negative']
print(negative_reviews)

print("-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----")

positive_reviews = result_df[result_df['sentiment'] == 'positive']
print(positive_reviews)
result_df.to_csv('sentiment_analysis_result.csv',index=False, encoding='utf-8-sig')
negative_reviews.to_csv('negative_review.csv',index=False, encoding='utf-8-sig')
positive_reviews.to_csv('positive_review.csv',index=False, encoding='utf-8-sig')
