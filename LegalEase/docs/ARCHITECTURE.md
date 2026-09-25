# LegalEase Documentation

## Architecture & Workflow
1. **Frontend**: Streamlit interactive UI (`frontend/app.py`)
2. **Backend**: FastAPI REST API (`legalEaseAPI/main.py`, `legalEaseAPI/routes.py`)
3. **AI Core**: Gemini 1.5 Pro Generator (`ai_core/gemini_generator.py`)
4. **Formatters**: DOCX, PDF, and HTML preview engine (`ai_core/generator.py`)

## Export Formats
- `.txt`: Plain text representation
- `.docx`: Microsoft Word formatted document with embedded header logo and footer
- `.pdf`: Standard printable PDF format with headers, footers, and page numbers
