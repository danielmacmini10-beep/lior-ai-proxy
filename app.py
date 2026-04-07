from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

SHOPIFY_STORE = "phaqdr-wq.myshopify.com"
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def home(): return 'Lior AI Proxy is running!'

@app.route('/ai', methods=['POST', 'OPTIONS'])
def ai_proxy():
    if request.method == 'OPTIONS': return '', 200
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        response = requests.post('https://api.anthropic.com/v1/messages',
            headers={'x-api-key': os.environ.get('ANTHROPIC_API_KEY'),
                     'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
            json={'model': 'claude-sonnet-4-20250514', 'max_tokens': 1500,
                  'messages': [{'role': 'user', 'content': prompt}]}, timeout=60)
        return jsonify({'result': response.json()['content'][0]['text']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shopify', methods=['GET', 'OPTIONS'])
def shopify_proxy():
    if request.method == 'OPTIONS': return '', 200
    try:
        endpoint = request.args.get('endpoint', '')
        params = request.args.to_dict()
        params.pop('endpoint', None)
        
        url = f"https://{SHOPIFY_STORE}/admin/api/2026-01/{endpoint}.json"
        response = requests.get(url,
            headers={
                'X-Shopify-Access-Token': SHOPIFY_TOKEN,
                'Content-Type': 'application/json'
            },
            params=params,
            timeout=30)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
