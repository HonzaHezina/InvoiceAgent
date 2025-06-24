from tools.ocr_tool import extract_text_from_invoice

class InvoiceReaderAgent:
    def run(self, image_path):
        print(f"[Agent] Spouštím OCR na {image_path}")
        text = extract_text_from_invoice(image_path)
        return text