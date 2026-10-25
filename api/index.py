from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == 'my_secure_verify_token_123':
            return challenge, 200
        return "Verification failed", 403
    
    return "Event received", 200

if __name__ == '__main__':
    app.run()
