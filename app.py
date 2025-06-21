from flask import Flask, request, jsonify
#from mistral import call_mistral

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
    #prompt = f"An email was received:\nSubject: {subject}\nBody: {body}\n\nWrite a professional reply:"
    #reply = call_mistral(prompt) commit test

    #print(f"Generated Reply for Case {case_id}:\n{reply}")
    return jsonify({"status": "success", "reply": 'reply sent'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
