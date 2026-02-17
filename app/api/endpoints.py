from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..workflow import app_graph
from ..utils import extract_pages_text

router = APIRouter()

@router.post("/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # Read file content
        content = await file.read()
        
        # Extract text from pages
        pages_text = extract_pages_text(content)
        
        # Initialize state
        initial_state = {
            "claim_id": claim_id,
            "pages": pages_text,
            "segregated_pages": {},
            "id_info": {},
            "discharge_summary": {},
            "itemized_bill": {},
            "final_result": {}
        }
        
        # Run LangGraph workflow
        result = app_graph.invoke(initial_state)
        
        return result.get("final_result", {"error": "Processing failed"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
