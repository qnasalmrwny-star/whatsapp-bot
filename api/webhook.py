from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == 'my_secure_verify_token_123':
                return challenge, 200
            else:
                return 'Verification failed', 403
        return 'Hello World', 200

    elif request.method == 'POST':
        data = request.json
        print(data)
        return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run()
