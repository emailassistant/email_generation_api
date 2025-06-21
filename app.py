import subprocess
import sys
from importlib.metadata import distributions

from flask import Flask, request, jsonify
#from mistral import call_mistral
from sentiment import analyze_sentiment

required = {
    'transformers',
    'torch',
    'scikit-learn',
    'protobuf',
    'tiktoken',
    'sentencepiece'  
}
installed = {dist.metadata['Name'].lower() for dist in distributions()}
missing = required - installed

if missing:
    print(f"Installing missing packages: {missing}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

app = Flask(__name__)

@app.route("/email-event", methods=["POST"])
def email_event():
    data = request.get_json()
    subject = data.get("Subject__c", "")
    body = data.get("Body__c", "")
    case_id = data.get("CaseId__c", "")
    
    print("📩 New Email Event Received")
    print("CaseId:", case_id)
    print("Subject:", subject)
    print("Body:", body)
    prompt = f"An email was received:\nSubject: {subject}\nBody: {body}\n\nSentiment:"
    sentiment, confidence = analyze_sentiment(prompt)
    reply = f"Text: {prompt}\nSentiment: {sentiment} (Confidence: {confidence})\n"
    print(reply)
    
    #prompt = f"An email was received:\nSubject: {subject}\nBody: {body}\n\nWrite a professional reply:"
    #reply = call_mistral(prompt) test commit 123 45678

    #print(f"Generated Reply for Case {case_id}:\n{reply}")
    return jsonify({"status": "success", "reply": reply}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
