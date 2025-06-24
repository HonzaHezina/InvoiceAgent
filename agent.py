import requests
import base64
import os

# Nastav si svůj HF token jako proměnnou prostředí nebo přímo zde
HUGGINGFACE_TOKEN = os.environ.get("HF_TOKEN", "hf_...")
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-VL-32B-Instruct"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Accept": "application/json"
}

def load_image_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def query_image(prompt, image_path):
    image_b64 = load_image_base64(image_path)
    payload = {
        "inputs": [
            {"type": "image", "image": image_b64},
            {"type": "text", "text": prompt}
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    image_path = "invoice.jpg"
    prompt = "Vyextrahuj veškerý text z této faktury a vypiš ho česky jako plain text."
    result = query_image(prompt, image_path)
    print("Výsledek:")
    print(result)
