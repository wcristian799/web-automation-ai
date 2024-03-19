from flask import Blueprint, request, jsonify
import openai

bp = Blueprint('news_summarizer', __name__, url_prefix='/summarize')

@bp.route('/', methods=['POST'])
def summarize():
    data = request.json
    openai.api_key = request.app.config['OPENAI_API_KEY']

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Faça um resumo deste texto: {data['text']}",
        max_tokens=150,
        temperature=0.5
    )
    summary = response.choices[0].text.strip()

    return jsonify({"message": "Sumário gerado com sucesso.", "summary": summary})
