# LegalEase: AI-Powered Legal Document Generator

LegalEase leverages Generative AI (Google Gemini 1.5 Pro) to simplify the creation of structured, accurate, and editable legal documents. Users can generate Employment Contracts, Lease Agreements, Non-Disclosure Agreements (NDAs), and Freelance Agreements tailored to specific parties, effective dates, and contractual clauses.

---

## 🏛️ Project Architecture

```
LegalEase/
├── ai_core/
│   ├── __init__.py
│   ├── gemini_generator.py      # Google Gemini 1.5 Pro AI integration & templates
│   └── generator.py             # Formatters: DOCX, PDF, HTML preview & text sanitization
├── frontend/
│   └── app.py                   # Modern Streamlit web application interface
├── image/
│   ├── Logo.png                 # LegalEase official branded logo
│   └── inverseLogo.png          # Dark mode branded logo
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                  # FastAPI server application & CORS configuration
│   └── routes.py                # POST /generate & health endpoints
├── .env                         # Environment variables (API keys, ports)
├── .env.example                 # Example environment configuration
├── config.py                    # Global configuration loader
├── requirements.txt             # Python dependencies
├── run.bat                      # Windows launcher script
└── run.sh                       # Linux / Mac launcher script
```

---

## 🚀 Key Features

- **AI-Powered Legal Drafting**: Generates formal agreements with standard preambles, recitals, defined terms, structured clauses, and signature blocks.
- **Dynamic HTML Preview**: Live, dark-mode preview of the generated legal agreement with highlighted sections.
- **Inline Editing**: Allows users to customize terms directly in the app before exporting.
- **Multi-Format Document Export**:
  - **.TXT** – Clean plain text.
  - **.DOCX** – Formatted Microsoft Word document with embedded logo, Times New Roman font, and standard margins.
  - **.PDF** – Ready-to-use branded PDF with header logo and footer on all pages.
- **Preset Scenarios**: One-click loaders for Freelance Work Contracts, NDAs, Residential Leases, and Employment Contracts.

---

## 🛠️ Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and add your Gemini API Key:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

---

## 🏃 Running the Application

### Option 1: Automatic Launch (Windows)
Double-click `run.bat` or run:
```powershell
.\run.bat
```

### Option 2: Manual Launch

1. **Start the FastAPI Backend**:
```bash
python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Start the Streamlit Frontend**:
```bash
streamlit run frontend/app.py
```

- **Frontend URL**: [http://localhost:8501](http://localhost:8501)
- **Backend API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
