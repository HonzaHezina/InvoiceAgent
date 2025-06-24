import requests, base64, os

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-VL-32B-Instruct"

def extract_text_from_invoice(image_path, prompt):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": [
            {"type": "image", "image": img_b64},
            {"type": "text", "text": prompt}
        ]
    }

    resp = requests.post(API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json().get("generated_text", "No text found.")