import os
import requests
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# --- إعدادات مفاتيح الربط الخاصة بك ---
GEMINI_API_KEY = "AQ.Ab8RN6JRzd5QpLnb3y2NmhV0ayCVRIMHAIGmwFuT_Um58osaPA"
WHATSAPP_TOKEN = "EAGbZBMps7wHcBS9Vu3nhdJtZAB4fQYPOZAmhElLbjYw3aqHBzbyFmxQqq0U3HjgYb9oZCHfY7MUiAQ8U3HegwUIq47acLQ1XCCrGMMdKtT2LqRLql7XbT2SZCawFGlxKXlEcubjzW0cB1J9kck8BZCnAMrYRHPA4PHk0ld7mRZAbNqKZAeFTEQW4SEYOu9FqfpyDIbg7sUKZCEmqhXWpmZAfpxWx2SvksaULFKCZBM082L4wLwo2sR9QlyDGgijJdDZBxb64tuBnsfatN91GZCZCSZAhOLsj3Gv7p0ZD"
PHONE_NUMBER_ID = "1310742642132559"
VERIFY_TOKEN = "my_secure_verify_token_123"

# تهيئة عميل الذكاء الاصطناعي
client = genai.Client(api_key=GEMINI_API_KEY)

# تعليمات النظام التي صممناها سابقاً
system_instruction = """
أنت "معلم برمجة ذكي وصبور"، مصمم خصيصاً لمساعدة الطلاب المبتدئين في تعلم لغات البرمجة عبر تطبيق واتساب. 
القواعد الصارمة التي يجب أن تلتزم بها في كل رد:
1. التخصص المطلق: أجب فقط على الأسئلة المتعلقة ببرمجة الكمبيوتر، لغات البرمجة، المفاهيم البرمجية، وتصحيح الأكواد (Debugging). إذا سأل المستخدم عن أي موضوع آخر خارج البرمجة، اعتذر ووجهه لطرح سؤال برمجي.
2. ضرب أمثلة واقعية: قبل أو أثناء شرح أي مفهوم برمجي، قم فوراً بضرب مثال من الحياة اليومية المألوفة لتسهيل الفهم على المبتدئين.
3. التبسيط والتنظيم لشاشة الهاتف: اجعل إجاباتك قصيرة، مركزة، ومقسّمة إلى خطوات واضحة لتكون سهلة القراءة على شاشة الجوال.
4. تنسيق الأكواد: عندما تعرض كوداً برمجياً، استخدم دائماً علامات التنسيق أحادية المسافة (```) لضمان وضوحه، وقم بتفكيك الكود وشرح كل سطر ببساطة.
5. التشجيع المستمر: استخدم نبرة صوت دافئة ومشجعة للمبتدئين لتكسر حاجز الخوف لديهم من البرمجة.
"""

def ask_ai_teacher(user_message):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return "عذراً، حدث خطأ بسيط أثناء معالجة سؤالك البرمجي. حاول مرة أخرى!"

def send_whatsapp_message(recipient_phone, message_text):
    url = f"[https://graph.facebook.com/v18.0/](https://graph.facebook.com/v18.0/){PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {"body": message_text}
    }
    requests.post(url, json=payload, headers=headers)

# --- مسار التحقق من Webhook (مطلوب من ميتا) ---
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403
    return "Hello World", 200

# --- مسار استقبال رسائل واتساب ---
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            message_data = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender_phone = message_data["from"] # رقم الطالب
            user_message = message_data["text"]["body"] # نص السؤال البرمجي

            # استدعاء الذكاء الاصطناعي للحصول على الشرح المفصل والأمثلة الواقعية
            ai_reply = ask_ai_teacher(user_message)

            # إرسال الرد للطالب عبر واتساب
            send_whatsapp_message(sender_phone, ai_reply)
            
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
