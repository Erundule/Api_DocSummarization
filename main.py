import os
from api.controller import api_summarize, index, app
from config.config import Config
from flask import request, jsonify

#port config
port = int(os.environ.get('PORT', 8080))

#authorization
app.config.from_object(Config)

def authenticate_api_key(api_key):
    return api_key in app.config['VALID_API_KEYS']

@app.before_request
def check_api_key():
    if request.endpoint == 'api_summarize':
        api_key = request.headers.get('Api-Key')
        print(f"Received API key: {api_key}")  
        if not api_key or not authenticate_api_key(api_key):
            return jsonify({'error': 'Unauthorized. Invalid API key.'}), 401
        
#api routes
app.add_url_rule('/summarize', 'api_summarize', api_summarize, methods=['POST'])
app.add_url_rule('/', 'index', index, methods=['GET'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

