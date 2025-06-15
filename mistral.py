import requests
import os

TOGETHER_API_KEY = os.getenv("tgp_v1_9cSNx9v3VRIJ8_WkAJl0c33j0Lg7H1E6l77RtQG2HXE")

def call_mistral(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip()
