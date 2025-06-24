from tools.ocr_tool import extract_text_from_invoice

class InvoiceReaderAgent:
    PROMPT = "Extract all visible text from this invoice in plain text."

    def run(self, image_path):
        print(f"[Agent] Spouštím OCR na {image_path}")
        return extract_text_from_invoice(image_path, self.PROMPT)