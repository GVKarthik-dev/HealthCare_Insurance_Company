import os
from typing import List, Dict, Any, TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from .models import IDInformation, DischargeSummary, ItemizedBill, ExtractionResult

load_dotenv()

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_KEY")
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile")

class GraphState(TypedDict):
    claim_id: str
    pages: List[str]
    segregated_pages: Dict[str, List[int]]  # doc_type -> list of page indices
    id_info: Dict[str, Any]
    discharge_summary: Dict[str, Any]
    itemized_bill: Dict[str, Any]
    final_result: Dict[str, Any]

from pydantic import BaseModel, Field

class PageClassification(BaseModel):
    page_index: int
    document_type: str = Field(description="One of: claim_forms, cheque_or_bank_details, identity_document, itemized_bill, discharge_summary, prescription, investigation_report, cash_receipt, other")

class SegregationResult(BaseModel):
    classifications: List[PageClassification]

SEGREGATOR_PROMPT = """
Analyze the content of the following pages from a medical claim document.
Classify each page into ONE of these categories:
- claim_forms
- cheque_or_bank_details
- identity_document
- itemized_bill
- discharge_summary
- prescription
- investigation_report
- cash_receipt
- other

Provide the result as a JSON object matching this schema:
{format_instructions}

Pages Text:
{pages_text}
"""

def segregator_agent(state: GraphState) -> Dict[str, Any]:
    pages = state["pages"]
    # We'll pass a summary or snippets if too many pages
    pages_input = "\n\n".join([f"Page {i}: {text[:1500]}" for i, text in enumerate(pages)])
    
    parser = JsonOutputParser(pydantic_object=SegregationResult)
    prompt = ChatPromptTemplate.from_template(SEGREGATOR_PROMPT)
    chain = prompt | llm | parser
    
    result = chain.invoke({
        "pages_text": pages_input,
        "format_instructions": parser.get_format_instructions()
    })
    
    segregated = {
        "claim_forms": [],
        "cheque_or_bank_details": [],
        "identity_document": [],
        "itemized_bill": [],
        "discharge_summary": [],
        "prescription": [],
        "investigation_report": [],
        "cash_receipt": [],
        "other": []
    }
    
    for item in result.get("classifications", []):
        doc_type = item["document_type"]
        page_idx = item["page_index"]
        if doc_type in segregated:
            segregated[doc_type].append(page_idx)
    
    return {"segregated_pages": segregated}

# --- Extraction Agents ---

def id_agent(state: GraphState) -> Dict[str, Any]:
    indices = state["segregated_pages"].get("identity_document", [])
    if not indices:
        return {"id_info": {}}
    
    text = "\n\n".join([state["pages"][i] for i in indices])
    
    prompt = ChatPromptTemplate.from_template(
        "Extract patient identification info from this text. IMPORTANT: Ensure the output is valid JSON. Output as JSON matching: {format_instructions}\n\nText:\n{text}"
    )
    parser = JsonOutputParser(pydantic_object=IDInformation)
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"text": text, "format_instructions": parser.get_format_instructions()})
        return {"id_info": result}
    except Exception as e:
        print(f"Error in id_agent: {e}")
        return {"id_info": {}}

def discharge_summary_agent(state: GraphState) -> Dict[str, Any]:
    indices = state["segregated_pages"].get("discharge_summary", [])
    if not indices:
        return {"discharge_summary": {}}
    
    text = "\n\n".join([state["pages"][i] for i in indices])
    
    prompt = ChatPromptTemplate.from_template(
        "Extract discharge summary details from this text. IMPORTANT: Ensure the output is valid JSON. Output as JSON matching: {format_instructions}\n\nText:\n{text}"
    )
    parser = JsonOutputParser(pydantic_object=DischargeSummary)
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"text": text, "format_instructions": parser.get_format_instructions()})
        return {"discharge_summary": result}
    except Exception as e:
        print(f"Error in discharge_summary_agent: {e}")
        return {"discharge_summary": {}}

def itemized_bill_agent(state: GraphState) -> Dict[str, Any]:
    indices = state["segregated_pages"].get("itemized_bill", [])
    if not indices:
        return {"itemized_bill": {}}
    
    text = "\n\n".join([state["pages"][i] for i in indices])
    
    prompt = ChatPromptTemplate.from_template(
        "Extract itemized billing details from this text. Calculate the final total amount if not explicitly stated. \n"
        "IMPORTANT: The 'total_amount' field must be a single FLOAT or INT value. Do NOT include mathematical expressions like 'A + B'. \n"
        "Output as JSON matching: {format_instructions}\n\nText:\n{text}"
    )
    parser = JsonOutputParser(pydantic_object=ItemizedBill)
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"text": text, "format_instructions": parser.get_format_instructions()})
        return {"itemized_bill": result}
    except Exception as e:
        print(f"Error in itemized_bill_agent: {e}")
        return {"itemized_bill": {}}

# --- Aggregator ---

def aggregator_node(state: GraphState) -> Dict[str, Any]:
    final_json = {
        "claim_id": state["claim_id"],
        "extracted_data": {
            "identity_information": state.get("id_info", {}),
            "discharge_summary": state.get("discharge_summary", {}),
            "itemized_bill": state.get("itemized_bill", {})
        },
        "document_segregation": state["segregated_pages"]
    }
    return {"final_result": final_json}
