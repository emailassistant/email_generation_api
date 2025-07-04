from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Lightweight 3-class sentiment model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Mapping class index to sentiment label
# Updated id2label to include mapping for class index 2
id2label = {0: "negative", 1: "neutral", 2: "positive"}

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


