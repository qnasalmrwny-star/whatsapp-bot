from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token == 'my_secure_verify_token_123':
            return challenge, 200
        return 'Hello World', 200

    elif request.method == 'POST':
        return jsonify({"status": "received"}), 200

@app.route('/', methods=['GET'])
def home():
    return 'Hello World', 200
