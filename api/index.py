import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# رموز المصادقة والتحقق
ACCESS_TOKEN = "EAGbZBMps7wHcBSyBWw4LZAPnwIPoGeZCELv26RcKSX3xVnJ0r6DY2HySPJe356HDJfe56DZAQQfYwbxAUPoeWYPIZAAatMND5TxG3B3epPcfRGHx0fRNMCB94jiIHVRJ1KcYHCeySWpJxm69ZBH3w5M9UC8X2Rn0cbZCNZABB7crAZC6SC0szIuVZBg0ElavF627L0ESCkTDFS5HcTGKGmAOZBbflCZBHRot2ZBDtqA9MtfPvp0PtqJMmTIZBonC063aGiBhhrnOTPPe9guNEcSECQUq9unAuE"
VERIFY_TOKEN = "my_secure_verify_token_123"


@app.route("/", methods=["GET"])
def home():
  return "WhatsApp Bot Server is Active!"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  if request.method == "GET":
    # التحقق من الويب هوك بواسطة ميتا
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
      if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge, 200
      else:
        return "Verification failed", 403
    return "Hello, this is the webhook endpoint", 200

  elif request.method == "POST":
    # استقبال رسائل واتساب الواردة
    body = request.get_json()
    print(json.dumps(body, indent=4))

    try:
      if body.get("object"):
        if (
            body.get("entry")
            and body["entry"][0].get("changes")
            and body["entry"][0]["changes"][0].get("value")
            and body["entry"][0]["changes"][0]["value"].get("messages")
        ):

          phone_number_id = body["entry"][0]["changes"][0]["value"]["metadata"][
              "phone_number_id"
          ]
          from_wa_id = body["entry"][0]["changes"][0]["value"]["messages"][0][
              "from"
          ]
          msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0][
              "text"
          ]["body"]

          # إرسال رد تلقائي عبر واتساب
          url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
          headers = {
              "Authorization": f"Bearer {ACCESS_TOKEN}",
              "Content-Type": "application/json",
          }
          data = {
              "messaging_product": "whatsapp",
              "to": from_wa_id,
              "text": {
                  "body": (
                      f"أهلاً بك! لقد استلمت رسالتك بنجاح: '{msg_body}'"
                  )
              },
          }

          response = requests.post(url, headers=headers, json=data)
          print(response.json())

        return "EVENT_RECEIVED", 200
      else:
        return "Not a valid webhook event", 404
    except Exception as e:
      print(f"Error handling webhook: {e}")
      return "Internal Server Error", 500


if __name__ == "__main__":
  app.run(debug=True)
