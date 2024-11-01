from flask import Flask, request, jsonify
import automatic_summarizer as summarizer
import json

app = Flask(__name__)

@app.route('/summarize-news', methods=['POST'])
def summarize_news():
    data = request.json
    url = data['url']
    link_selector = data.get('link_selector', 'a.focusIndicatorDisplayBlock.bbc-uk8dsi.e1d658bg0')
    content_selector = data.get('content_selector', 'div#story-body p')
    
    driver = summarizer.setup_driver(headless=True)
    news_data = summarizer.fetch_news(driver, url, link_selector, 5)
    summaries = summarizer.process_news(driver, news_data, content_selector)
    driver.quit()

    ranked_summaries = summarizer.rank_summaries_by_length_and_sentiment(summaries)
    
    # Opcional: converter os resumos classificados para JSON e retornar
    json_output = json.dumps(ranked_summaries, ensure_ascii=False, indent=2)
    
    return jsonify(json_output)

if __name__ == '__main__':
    app.run(debug=True)
