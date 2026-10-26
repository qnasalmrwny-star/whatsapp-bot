import json
import urllib.request
from flask import Flask, request

app = Flask(__name__)

# رمز الوصول الخاص بك المدمج جاهزاً
ACCESS_TOKEN = "EAGbZBMps7wHcBSZBfFqS62rhZCw85c9ZBojZANVMp7RvbfqR1ZCmOWVZAZAPWZAOKmC2sZC56w1SvIzrvlczVtUKp2zoMbatCOTlAH69RaY64jc1xpgJDiFbNfBopf8vEPEnLgFtxydArpux4fG3I1NYNTqqSDz8EEvrxZBdCfos1cpEZBc1TSSgwgUOdi1xDiocN8GZC1yHnaZCxRf2QdtTQXP9iOmYmokZCFEJjp0QCZBQpVQyxVagmTiscoSAcdiOluv2oykFnFOS1rVj4zYaDwc5vNPQnKU0YgZDZD"

@app.route('/')
def home():
    return "Bot is running successfully!"

@app.route('/webhook', methods=['GET', 'POST'])
@app.route('/api/index', methods=['GET', 'POST'])
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
            
    # استقبال الرسائل الواردة من واتساب والرد عليها (POST)
    elif request.method == 'POST':
        body = request.get_json()
        print("WEBHOOK BODY RECEIVED:", body)
        
        try:
            value = body['entry'][0]['changes'][0]['value']
            if 'messages' in value:
                phone_number_id = value['metadata']['phone_number_id']
                from_number = value['messages'][0]['from']
                msg_body = value['messages'][0]['text']['body']
                print(f"Message from {from_number}: {msg_body}")
                
                # إرسال رد تلقائي للمستخدم
                reply_text = f"أهلاً بك! لقد استلمت رسالتك: \"{msg_body}\""
                send_whatsapp_message(phone_number_id, from_number, reply_text)
        except Exception as e:
            print("Error processing message:", e)
            
        return "EVENT_RECEIVED", 200

def send_whatsapp_message(phone_number_id, recipient_phone, message_text):
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "text": {"body": message_text}
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            print("Message sent response:", response.read().decode('utf-8'))
    except Exception as e:
        print("Failed to send message:", e)

if __name__ == '__main__':
    app.run()
