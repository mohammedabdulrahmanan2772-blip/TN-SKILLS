import io
import sys
from fastapi.testclient import TestClient

from legalEaseAPI.main import app
from ai_core.gemini_generator import GeminiDocumentGenerator
from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview

def test_all():
    print("=== 1. Testing Gemini Document Generator ===")
    generator = GeminiDocumentGenerator()
    doc = generator.generate_document(
        document_type="Freelance Work Contract",
        parties="Jane Doe (Service Provider), TechNova Inc. (Client)",
        terms="Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; Client retains intellectual property rights; Either party may terminate with 15 days notice",
        dates="April 15, 2025"
    )
    assert doc and len(doc) > 100
    print("[PASS] Document generated successfully (Length:", len(doc), "chars)")

    print("\n=== 2. Testing Text Sanitizer ===")
    sample_text = '“Smart quotes” and ‘single quotes’ — dash…'
    sanitized = sanitize_text(sample_text)
    print("Sanitized:", sanitized)
    assert '"' in sanitized and "'" in sanitized

    print("\n=== 3. Testing DOCX Generation ===")
    docx_io = format_docx(doc, "Freelance Work Contract")
    docx_bytes = docx_io.getvalue()
    assert len(docx_bytes) > 1000
    print("[PASS] DOCX generated successfully (Bytes:", len(docx_bytes), ")")

    print("\n=== 4. Testing PDF Generation ===")
    pdf_io = format_pdf(doc, "Freelance Work Contract")
    pdf_bytes = pdf_io.getvalue()
    assert len(pdf_bytes) > 1000
    print("[PASS] PDF generated successfully (Bytes:", len(pdf_bytes), ")")

    print("\n=== 5. Testing HTML Preview ===")
    html = format_html_preview(doc)
    assert "</h2>" in html or "</h3>" in html or "<p" in html
    print("[PASS] HTML Preview generated successfully")

    print("\n=== 6. Testing FastAPI Endpoints ===")
    client = TestClient(app)
    
    # Test Root
    res_root = client.get("/")
    assert res_root.status_code == 200
    print("[PASS] Root endpoint status 200:", res_root.json())
    
    # Test /generate
    res_gen = client.post("/generate", json={
        "document_type": "Non-Disclosure Agreement (NDA)",
        "parties": "Company A, Company B",
        "terms": "Mutual confidentiality for 2 years",
        "dates": "January 1, 2026"
    })
    assert res_gen.status_code == 200
    assert "document" in res_gen.json()
    print("[PASS] /generate endpoint status 200: Generated length:", len(res_gen.json()["document"]))

    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_all()
