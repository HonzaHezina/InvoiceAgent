from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Address(BaseModel):
    StreetName: Optional[str]
    BuildingNumber: Optional[str]
    CityName: Optional[str]
    PostalZone: Optional[str]
    Country: Dict[str, Optional[str]]

class Contact(BaseModel):
    Telephone: Optional[str]
    ElectronicMail: Optional[str]

class Party(BaseModel):
    PartyIdentification: Dict[str, Optional[str]]
    PartyName: Dict[str, Optional[str]]
    PostalAddress: Address
    PartyTaxScheme: Dict[str, Optional[str]]
    Contact: Contact

class InvoiceLine(BaseModel):
    ID: str
    InvoicedQuantity: float
    LineExtensionAmount: float
    LineExtensionAmountTaxInclusive: float
    LineExtensionTaxAmount: float
    UnitPrice: float
    UnitPriceTaxInclusive: float
    ClassifiedTaxCategory: Dict[str, Optional[float]]
    Item: Dict[str, Optional[str]]

class InvoiceLines(BaseModel):
    InvoiceLine: List[InvoiceLine]

class TaxCategory(BaseModel):
    Percent: float
    VATApplicable: bool

class TaxSubTotal(BaseModel):
    TaxableAmount: float
    TaxAmount: float
    TaxInclusiveAmount: float
    TaxCategory: TaxCategory

class TaxTotal(BaseModel):
    TaxSubTotal: TaxSubTotal
    TaxAmount: float

class LegalMonetaryTotal(BaseModel):
    TaxExclusiveAmount: float
    TaxInclusiveAmount: float
    PayableAmount: float

class PaymentDetails(BaseModel):
    PaymentDueDate: Optional[str]
    ID: Optional[str]
    BankCode: Optional[str]
    VariableSymbol: Optional[int]

class Payment(BaseModel):
    PaidAmount: float
    PaymentMeansCode: int
    Details: PaymentDetails

class PaymentMeans(BaseModel):
    Payment: Payment

class InvoiceDocument(BaseModel):
    DocumentType: int
    ID: str
    IssuingSystem: str
    IssueDate: str
    TaxPointDate: str
    VATApplicable: bool
    AccountingSupplierParty: Dict[str, Party]
    AccountingCustomerParty: Dict[str, Party]
    InvoiceLines: InvoiceLines
    TaxTotal: TaxTotal
    LegalMonetaryTotal: LegalMonetaryTotal
    PaymentMeans: PaymentMeans