from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import openai
import time
import json

# Configura a chave da API do OpenAI
openai.api_key = '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'

def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def fetch_news(driver, url, link_selector, limit=5):
    driver.get(url)
    time.sleep(1)
    news_links = driver.find_elements(By.CSS_SELECTOR, link_selector)[:limit]
    news_data = [(link.text, link.get_attribute('href')) for link in news_links]
    return news_data

def summarize_content(content):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Summarize this content in Portuguese, capturing the essence of the text with a human-like and direct approach, without including additional explanations:\n\n{content}",
        temperature=0.7,  #Temperatura mais volátio para um compartamento humano
        max_tokens=400  # Limite ideal
    )
    return response.choices[0].text.strip()

def analyze_sentiment(summary):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Given the following summary, classify the sentiment as either 'Positive', 'Neutral', or 'Negative':\n\n{summary}",
        temperature=0.3,  # Temperatura mais baixa para ter uma resposta direta
        max_tokens=60  # Tokens reduzido para uma resposta mais curta
    )
    sentiment_analysis = response.choices[0].text.strip()
    return sentiment_analysis

def process_news(driver, news_data, content_selector):
    summaries = []
    for title, href in news_data:
        driver.get(href)
        time.sleep(1)
        content_elements = driver.find_elements(By.CSS_SELECTOR, content_selector)
        content = ' '.join([el.text for el in content_elements if el.text])
        summary = summarize_content(content)
        sentiment_analysis = analyze_sentiment(summary)
        summaries.append({'title': title, 'summary': summary, 'sentiment_analysis': sentiment_analysis})
    return summaries

def rank_summaries_by_length_and_sentiment(all_summaries):
    # Convertendo análise de sentimentos em um score numérico simples para simplificação
    sentiment_score = {'Positive': 2, 'Neutral': 1, 'Negative': 0}

    # Adicionando um score baseado no comprimento do resumo
    for summary in all_summaries:
        summary_length = len(summary['summary'])
        summary['score'] = summary_length * sentiment_score.get(summary['sentiment_analysis'], 1)

    # Classificando os resumos baseado no score calculado
    ranked_summaries = sorted(all_summaries, key=lambda x: x['score'], reverse=True)
    return ranked_summaries

def present_ranked_summaries(ranked_summaries):
    for summary in ranked_summaries:
        print(f"Title: {summary['title']}\nSummary: {summary['summary']}\nSentiment: {summary['sentiment_analysis']}\nScore: {summary['score']}\n")

if __name__ == "__main__":
    driver = setup_driver(headless=False)
    news_sites = [
        {'name': 'BBC', 'url': 'https://www.bbc.com/portuguese', 'link_selector': 'a.focusIndicatorDisplayBlock.bbc-uk8dsi.e1d658bg0', 'content_selector': 'div#story-body p'},
        {'name': 'CNN Brasil', 'url': 'https://www.cnnbrasil.com.br/', 'link_selector': '.homepage__blocks__list a', 'content_selector': '.post__content p'}
    ]

    all_summaries = []
    for site in news_sites:
        news_data = fetch_news(driver, site['url'], site['link_selector'])
        summaries = process_news(driver, news_data, site['content_selector'])
        all_summaries.extend(summaries)

    driver.quit()

    ranked_summaries = rank_summaries_by_length_and_sentiment(all_summaries)
    present_ranked_summaries(ranked_summaries)

     # Convertendo para JSON
    json_output = json.dumps(ranked_summaries, ensure_ascii=False, indent=2)
    print(json_output)
 