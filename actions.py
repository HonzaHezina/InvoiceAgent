import requests, base64, os

HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-VL-32B-Instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}", "Accept": "application/json"}

def ocr_extract(image_path):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    payload = {
        "inputs": [
            {"type": "image", "image": img_b64},
            {"type": "text", "text": "Vyextrahuj text z faktury jako plain text."}
        ]
    }
    resp = requests.post(API_URL, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json().get("generated_text", "")
