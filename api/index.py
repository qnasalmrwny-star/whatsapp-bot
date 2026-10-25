from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # التحقق من الويب هوك الخاص بـ Meta (GET)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == 'my_secure_verify_token_123':
            return challenge, 200
        else:
            return "Verification failed", 403
            
    # استلام رسائل واتساب لاحقاً (POST)
    elif request.method == 'POST':
        data = request.json
        return "EVENT_RECEIVED", 200

if __name__ == '__main__':
    app.run()
