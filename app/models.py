from pydantic import BaseModel, Field
from typing import List, Optional

class IDInformation(BaseModel):
    patient_name: Optional[str] = Field(None, description="Name of the patient")
    dob: Optional[str] = Field(None, description="Date of birth")
    id_number: Optional[str] = Field(None, description="Identification number (Aadhar, PAN, etc.)")
    policy_details: Optional[str] = Field(None, description="Insurance policy details")

class DischargeSummary(BaseModel):
    diagnosis: Optional[str] = Field(None, description="Primary diagnosis")
    admission_date: Optional[str] = Field(None, description="Date of admission")
    discharge_date: Optional[str] = Field(None, description="Date of discharge")
    physician_details: Optional[str] = Field(None, description="Attending physician details")

class BillItem(BaseModel):
    description: str
    cost: float

class ItemizedBill(BaseModel):
    items: List[BillItem]
    total_amount: float

class ExtractionResult(BaseModel):
    id_info: Optional[IDInformation] = None
    discharge_summary: Optional[DischargeSummary] = None
    itemized_bill: Optional[ItemizedBill] = None
