import json, openai, os
from actions import ocr_extract
from prompts import SYSTEM_PROMPT

openai.api_key = os.getenv("OPENAI_API_KEY")

FUNCTIONS = [
    {
        "name": "ocr_extract",
        "description": "Extract text from invoice image",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to invoice image"}
            },
            "required": ["image_path"]
        }
    }
]

def chat_loop(image_path):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Extract text from {image_path}"}
    ]
    for turn in range(3):  # max tři kroky
        resp = openai.ChatCompletion.create(
            model="gpt‑4‑oai‑function‑calling",
            messages=messages,
            functions=FUNCTIONS,
            function_call="auto"
        )
        msg = resp.choices[0].message
        if msg.get("function_call"):
            fn = msg.function_call
            args = json.loads(fn.arguments)
            result = None
            if fn.name == "ocr_extract":
                result = ocr_extract(**args)
            messages.append({"role": "function", "name": fn.name, "content": result})
            continue
        print("Answer:", msg.content)
        break

if __name__ == "__main__":
    chat_loop("invoice.jpg")
