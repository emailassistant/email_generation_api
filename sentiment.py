from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load pre-trained DeBERTa model and tokenizer
model_name = "microsoft/deberta-v3-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Mapping class index to sentiment label
id2label = {-1: "negative", 0: "neutral", 1: "positive"}

# Define the sentiment analysis function
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1)
        pred_class = torch.argmax(probs, dim=1).item()
        sentiment = id2label[pred_class]
        confidence = probs[0][pred_class].item()
        return sentiment, round(confidence, 2)

# Example usage
if __name__ == "__main__":
    texts = [
        "I'm very happy with your service!",
        "This was okay, not great but not bad either.",
        "I'm extremely disappointed and frustrated."
    ]

    for text in texts:
        sentiment, confidence = analyze_sentiment(text)
        print(f"Text: {text}\nSentiment: {sentiment} (Confidence: {confidence})\n")
