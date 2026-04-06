from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home():
    return 'Lior AI Proxy is running!'

@app.route('/ai', methods=['POST', 'OPTIONS'])
def ai_proxy():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return jsonify({'result': message.content[0].text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
