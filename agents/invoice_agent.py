import json
import requests
from tools.ocr_tool import extract_text_from_invoice, repair_json_if_invalid
from tools.invoice_model import InvoiceDocument

class InvoiceReaderAgent:
    PROMPT = """
Jsi specializovaný AI agent, který extrahuje data z naskenovaných faktur a účtenek. Vstupem je obrázek faktury nebo účtenky. Tvým úkolem je:

1. Rozpoznat veškeré klíčové informace.
2. Vrátit výstup jako platný JSON objekt podle níže uvedeného vzoru.
3. Pokud některé pole v dokumentu chybí, nahraď jej `null` nebo jej vynech.
4. Nepřidávej žádné komentáře nebo text mimo JSON výstup.

📄 JSON struktura, kterou máš vrátit (vyplň hodnoty podle faktury na obrázku):

{
  "DocumentType": 1,
  "ID": "<číslo faktury nebo dokladu>",
  "IssuingSystem": "scan",
  "IssueDate": "<datum vystavení>",
  "TaxPointDate": "<datum zdanitelného plnění>",
  "VATApplicable": true,
  "AccountingSupplierParty": {
    "Party": {
      "PartyIdentification": { "ID": "<IČ dodavatele>" },
      "PartyName": { "Name": "<název dodavatele>" },
      "PostalAddress": {
        "StreetName": "<ulice>",
        "BuildingNumber": "<číslo>",
        "CityName": "<město>",
        "PostalZone": "<PSČ>",
        "Country": { "IdentificationCode": "CZ", "Name": "" }
      },
      "PartyTaxScheme": {
        "CompanyID": "<DIČ dodavatele>",
        "TaxScheme": "VAT"
      },
      "Contact": {
        "Telephone": "<telefon dodavatele>",
        "ElectronicMail": "<e-mail dodavatele>"
      }
    }
  },
  "AccountingCustomerParty": {
    "Party": {
      "PartyIdentification": { "ID": "<IČ odběratele>" },
      "PartyName": { "Name": "<název odběratele>" },
      "PostalAddress": {
        "StreetName": "<ulice>",
        "BuildingNumber": "<číslo>",
        "CityName": "<město>",
        "PostalZone": "<PSČ>",
        "Country": { "IdentificationCode": "CZ", "Name": "" }
      },
      "PartyTaxScheme": {
        "CompanyID": "<DIČ odběratele>",
        "TaxScheme": "VAT"
      },
      "Contact": {
        "Telephone": "<telefon odběratele>",
        "ElectronicMail": "<e-mail odběratele>"
      }
    }
  },
  "InvoiceLines": {
    "InvoiceLine": [
      {
        "ID": "<číslo položky>",
        "InvoicedQuantity": <množství>,
        "LineExtensionAmount": <částka bez DPH>,
        "LineExtensionAmountTaxInclusive": <částka s DPH>,
        "LineExtensionTaxAmount": <DPH>,
        "UnitPrice": <jednotková cena bez DPH>,
        "UnitPriceTaxInclusive": <jednotková cena s DPH>,
        "ClassifiedTaxCategory": {
          "Percent": <sazba DPH>,
          "VATCalculationMethod": 0,
          "VATApplicable": true
        },
        "Item": { "Description": "<popis položky>" }
      }
    ]
  },
  "TaxTotal": {
    "TaxSubTotal": {
      "TaxableAmount": <základ DPH>,
      "TaxAmount": <částka DPH>,
      "TaxInclusiveAmount": <celkem s DPH>,
      "TaxCategory": {
        "Percent": <sazba DPH>,
        "VATApplicable": true
      }
    },
    "TaxAmount": <částka DPH>
  },
  "LegalMonetaryTotal": {
    "TaxExclusiveAmount": <celkem bez DPH>,
    "TaxInclusiveAmount": <celkem s DPH>,
    "PayableAmount": <k úhradě>
  },
  "PaymentMeans": {
    "Payment": {
      "PaidAmount": <zaplatit>,
      "PaymentMeansCode": 42,
      "Details": {
        "PaymentDueDate": "<datum splatnosti>",
        "ID": "<číslo účtu nebo referenční číslo>",
        "BankCode": "<kód banky>",
        "VariableSymbol": <VS>
      }
    }
  }
}

Vrať pouze JSON odpověď – bez úvodu, bez komentářů, bez vysvětlení.
"""

    def run(self, image_path):
        print(f"[Agent] Spouštím OCR na {image_path}")
        raw_result = extract_text_from_invoice(image_path, self.PROMPT)

        try:
            parsed_json = json.loads(raw_result)
        except json.JSONDecodeError:
            print("[Agent] JSON nevalidní, pokusím se opravit...")
            raw_result = repair_json_if_invalid(raw_result)
            parsed_json = json.loads(raw_result)

        try:
            invoice = InvoiceDocument(**parsed_json)
            print("[Agent] JSON validován.")
        except Exception as e:
            print("[Agent] Chyba validace JSON:", e)
            raise

        # Poslání přes API (dummy endpoint)
        try:
            response = requests.post("https://httpbin.org/post", json=parsed_json)
            print("[Agent] JSON odeslán přes API. Stav:", response.status_code)
        except Exception as e:
            print("[Agent] Chyba při odesílání JSON:", e)

        return parsed_json
