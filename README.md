# Financial Document Q&A Assistant

A Streamlit web application that processes financial documents (PDF and Excel), extracts key information, displays interactive visualizations, and provides a conversational question-answering interface using local Small Language Models (via Ollama) and retrieval-based techniques.

## Features

- Upload PDF and Excel files
- Robust PDF text + tables extraction (pdfplumber)
- Visualize numeric financial metrics with interactive Plotly charts (trend, comparison, correlation)
- Hybrid Q&A:
  - Fast rule-based lookup for structured tables (Pandas)
  - Retrieval-augmented QA using embeddings + Ollama LLM for unstructured PDF content
- Chat-style conversational UI with history
- Graceful fallbacks and helpful suggestions when exact answers are not found

## Project structure

project/
├─ app.py
├─ requirements.txt

├─ README.md

├─ .gitignore

├─ modules/

  ├─ extractor.py

  ├─ qa_engine.py

  ├─ visualizer.py

  └─ utils.py


## Prerequisites

- Python 3.9+
- Git
- (Optional) Git LFS for large sample files
- Ollama installed and running locally for LLM queries (if you want local LLM answers)

## Setup

1. Clone the repo (or create new repo and push your code)
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. Create a virtual environment and activate it:
  ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
 ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Install Ollama (for local LLM usage)
   - Download and install from https://ollama.com
   - Start Ollama and download a model, e.g.:
  ```bash
  ollama pull llama2
  ollama run llama2
  ```
   - For convenience, add Ollama to Windows Startup or run ollama serve in the background.

## Run the APP
```bash
streamlit run app.py
```
Open the URL printed by Streamlit (usually http://localhost:8501).

## How to use

Upload an Excel (.xlsx/.xls) or a PDF (annual report, financial statements).

#### If Excel:
  - Preview table and use the Visualization section to explore metrics.
  - Ask questions in the chat (structured lookups will run first).

#### If PDF:
  - The application will extract text and tables; ask questions in the chat.
  - The retrieval-augmented QA will search document chunks and answer via the local LLM.

Toggle the “Use AI (Ollama)” option to switch between rule-based and LLM-powered answers.

## Tips for testing

- Use small, clean Excel files to validate visualizations (columns: Month, Revenue, Expenses, Profit).
- For PDF testing, use annual reports or public 10-K PDFs.
- If answers look off, try rephrasing the query or enabling/disabling AI toggle.

## Troubleshooting

- Excel read errors (.xls): ensure xlrd or engine fallback is present. In extractor.py we try openpyxl first; for .xls install xlrd.
```bash
pip install xlrd openpyxl
```
- Ollama not found: ensure ollama is installed and in PATH. Run ollama --version.
- Embeddings/Chroma: first run may take time to build embedding DB. If Chroma persistent directory exists, remove .chroma/ to rebuild.

## Output
<img width="1890" height="844" alt="image" src="https://github.com/user-attachments/assets/1c554c0d-a2a4-4861-96cd-eefc1b0e0fca" />
