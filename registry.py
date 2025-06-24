from agents.invoice_agent import InvoiceReaderAgent

AGENT_REGISTRY = {
    "invoice_reader": InvoiceReaderAgent
}
from agents.businesscard_agent import BusinessCardReaderAgent
AGENT_REGISTRY["business_card_reader"] = BusinessCardReaderAgent
