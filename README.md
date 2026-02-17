# Medical Claim Form Processing API (LangGraph & Groq)

A high-performance FastAPI service that uses **LangGraph** and **Groq (Llama 3)** to orchestrate a multi-agent pipeline for medical claim processing and data extraction.

## 🚀 Pipeline Overview

This service implements a document-intelligent pipeline that segregates PDF pages and extracts structured data using specialized agents.

### LangGraph Workflow
`START` → `Segregator Agent (AI)` → (Parallel Extraction) → `Aggregator` → `END`

1.  **Segregator Agent (AI):**
    *   Analyzes the content of each page in the uploaded PDF.
    *   Classifies pages into 9 categories: `claim_forms`, `cheque_or_bank_details`, `identity_document`, `itemized_bill`, `discharge_summary`, `prescription`, `investigation_report`, `cash_receipt`, and `other`.
    *   Routes only the relevant pages to specialized extraction agents.

2.  **Extraction Agents (3 Required):**
    *   **ID Agent:** Extracts patient name, DOB, ID numbers, and policy details from `identity_document` pages.
    *   **Discharge Summary Agent:** Extracts diagnosis, admission/discharge dates, and physician details from `discharge_summary` pages.
    *   **Itemized Bill Agent:** Extracts all line items, costs, and calculates the total amount from `itemized_bill` pages.

3.  **Aggregator Node:**
    *   Consolidates the extracted JSON data from all agents.
    *   Returns a unified response including the final data and page segregation map.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Orchestration:** LangGraph
- **LLM:** Groq (Llama 3.3 70B)
- **PDF Processing:** PyPDF
- **Validation:** Pydantic

## 📂 Project Structure

```text
MEDICAL CLAIM FORM/
├── app/                  # Main application package
│   ├── api/              # API endpoints (planned for more complex apps)
│   ├── main.py           # FastAPI entry point
│   ├── agents.py         # Node logic for LangGraph agents
│   ├── workflow.py       # LangGraph state machine definition
│   ├── models.py         # Pydantic schemas
│   └── utils.py          # Utility functions (PDF parsing)
├── tests/                # Test cases for the pipeline
│   └── test_api.py       # Integration test for the /api/process endpoint
├── outputs/              # Directory for stored results and extracted JSONs
├── final.pdf             # Sample input file
├── run.py                # Convenience script to start the server
├── pyproject.toml        # Dependencies
└── .env                  # Environment variables (GROQ_KEY)
```

## ⚙️ Setup & Installation

1.  **Environment Variables:**
    Ensure you have a `.env` file with your Groq API key:
    ```env
    GROQ_KEY=your_groq_api_key_here
    ```

2.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn langgraph langchain-groq pypdf python-dotenv pydantic python-multipart requests
    ```

3.  **Run the Server:**
    ```bash
    python run.py
    ```

## 🧪 Testing

To test the pipeline manually:
1. Ensure the server is running.
2. Run the test script:
   ```bash
   python tests/test_api.py
   ```
3. Check the `outputs/` folder for the result.

## 📝 API Usage

### Process Claim
**Endpoint:** `POST /api/process`

**Parameters:**
- `claim_id` (string): Unique identifier for the claim.
- `file` (PDF): The medical claim PDF file.

**Sample Request (cURL):**
```bash
curl -X POST "http://localhost:8000/api/process" \
     -H "Content-Type: multipart/form-data" \
     -F "claim_id=CLM123" \
     -F "file=@final.pdf"
```

## 🎯 Features
- [x] **Page Segregation:** AI-powered classification of document types.
- [x] **Multi-Agent Extraction:** Parallel processing for increased efficiency.
- [x] **Structured Output:** Guaranteed JSON format using Pydantic parsers.
- [x] **Groq Integration:** Blazing fast inference with Llama 3 models.

---
*Developed for the Claim Processing Pipeline Assignment.*
