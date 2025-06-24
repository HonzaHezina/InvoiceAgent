import json
import requests
from tools.ocr_tool import extract_text_from_invoice, repair_json_if_invalid

class BusinessCardReaderAgent:
    PROMPT = """
Jsi inteligentní extrakční agent specializovaný na vytěžování kontaktních údajů z naskenovaných vizitek.

🔍 Tvůj úkol:
- Rozpoznat a extrahovat kontaktní údaje z obrázku vizitky.
- Vrať je jako platný JSON objekt se strukturou:

{
  "name": "<jméno osoby>",
  "title": "<pozice>",
  "company": "<firma>",
  "email": "<email>",
  "phone": "<telefon>",
  "address": "<adresa>",
  "website": "<webová stránka>"
}

📌 Pokud některý údaj chybí, nahraď hodnotou null.
Nezahrnuj žádné komentáře. Vrať pouze validní JSON výstup.
"""

    def run(self, image_path):
        print(f"[Agent] Spouštím OCR na vizitku {image_path}")
        raw_result = extract_text_from_invoice(image_path, self.PROMPT)

        try:
            parsed_json = json.loads(raw_result)
        except json.JSONDecodeError:
            print("[Agent] JSON nevalidní, pokusím se opravit...")
            raw_result = repair_json_if_invalid(raw_result)
            parsed_json = json.loads(raw_result)

        try:
            # API call
            response = requests.post("https://httpbin.org/post", json=parsed_json)
            print("[Agent] JSON odeslán přes API. Stav:", response.status_code)
        except Exception as e:
            print("[Agent] Chyba při odesílání JSON:", e)

        return parsed_json