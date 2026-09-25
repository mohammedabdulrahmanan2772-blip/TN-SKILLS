import os
import warnings
from config import GEMINI_API_KEY, MODEL_NAME

# Suppress deprecation warnings for cleaner runtime
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Try modern google.genai first, then fall back to google.generativeai
HAVE_GENAI_NEW = False
HAVE_GENAI_LEGACY = False

try:
    from google import genai
    from google.genai import types
    HAVE_GENAI_NEW = True
except Exception:
    try:
        import google.generativeai as genai_legacy
        HAVE_GENAI_LEGACY = True
    except Exception:
        pass

class GeminiDocumentGenerator:
    """
    Generates structured, high-quality legal documents using Google's Gemini models
    with fallback templates for reliable offline / zero-setup demonstrations.
    """
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name or MODEL_NAME or "gemini-1.5-pro"
        self.client_new = None
        self.legacy_model = None
        
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            if HAVE_GENAI_NEW:
                try:
                    self.client_new = genai.Client(api_key=self.api_key)
                except Exception as e:
                    print(f"[Warning] Failed to initialize google.genai Client: {e}")
            elif HAVE_GENAI_LEGACY:
                try:
                    genai_legacy.configure(api_key=self.api_key)
                    self.legacy_model = genai_legacy.GenerativeModel(self.model_name)
                except Exception as e:
                    print(f"[Warning] Failed to configure legacy google.generativeai: {e}")

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Generate a comprehensive, formal legal document from input parameters.
        """
        prompt = (
            f"You are an expert legal counsel and contract drafting assistant. "
            f"Generate a comprehensive, professional, legally sound document titled '{document_type}'.\n\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n\n"
            "Requirements:\n"
            "1. Use standard formal legal structure: Document Title (markdown ##), opening preamble with date and parties, RECITALS / WITNESSETH.\n"
            "2. Create numbered sections (e.g. 1. Definitions & Scope, 2. Term and Termination, 3. Payment and Consideration, 4. Intellectual Property, 5. Confidentiality, 6. Warranties and Liability, 7. Governing Law, 8. Miscellaneous).\n"
            "3. Incorporate all provided terms into clear, professional contractual clauses.\n"
            "4. Conclude with 'IN WITNESS WHEREOF' and clean signature blocks with blank signature lines for all involved parties.\n"
            "5. Return only clean markdown formatted legal text with clear headings and bullet points where appropriate."
        )

        # 1. Try modern google.genai SDK
        if self.client_new and self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                response = self.client_new.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[Gemini GenAI Notice] Call failed ({e}). Trying fallback...")

        # 2. Try legacy google.generativeai SDK
        if HAVE_GENAI_LEGACY and self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                if not self.legacy_model:
                    genai_legacy.configure(api_key=self.api_key)
                    self.legacy_model = genai_legacy.GenerativeModel(self.model_name)
                response = self.legacy_model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[Gemini Legacy Notice] Call failed ({e}). Using specialized legal template generator.")

        # 3. High-fidelity legal fallback generator (guarantees zero downtime & reliable demo)
        return self._generate_fallback_template(document_type, parties, terms, dates)

    def _generate_fallback_template(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Intelligent structured legal document template generator matching professional legal standards.
        """
        doc_title = document_type.strip() if document_type else "Legal Agreement"
        date_str = dates.strip() if dates else "the date of execution"
        
        # Parse parties
        party_lines = [p.strip() for p in parties.split(",") if p.strip()]
        if len(party_lines) >= 2:
            party_a = party_lines[0]
            party_b = ", ".join(party_lines[1:])
        elif party_lines:
            party_a = party_lines[0]
            party_b = "the other counterparty"
        else:
            party_a = "Party A"
            party_b = "Party B"

        # Parse terms
        raw_terms = [t.strip().rstrip(";") for t in terms.split(";") if t.strip()]
        if not raw_terms:
            raw_terms = [t.strip() for t in terms.split("\n") if t.strip()]
        if not raw_terms:
            raw_terms = [
                "The parties agree to fulfill all obligations outlined in this Agreement promptly and in good faith",
                "Payment shall be executed in accordance with agreed milestone schedules",
                "Confidential information disclosed by either party must be maintained with strict confidentiality",
                "Either party may terminate this agreement with 15 days written notice upon material breach"
            ]

        terms_clauses = ""
        for idx, term in enumerate(raw_terms, 1):
            terms_clauses += f"  - **Clause {idx}.{idx}**: {term}.\n"

        doc = f"""## {doc_title.upper()}

This {doc_title} (the "Agreement") is entered into and made effective as of **{date_str}** (the "Effective Date"), by and between:

**Party One:** {party_a}
**Party Two:** {party_b}

(Collectively referred to herein as the "Parties" and individually as a "Party").

### WITNESSETH:
WHEREAS, the Parties wish to establish the formal terms, rights, covenants, and responsibilities governing their relationship as described herein; and
WHEREAS, both Parties possess full legal capacity and corporate authority to enter into this legally binding Agreement;

NOW, THEREFORE, in consideration of the mutual covenants and promises set forth herein, the Parties agree as follows:

1. **Scope and Core Obligations:**
The Parties hereby agree to perform their respective covenants, deliverables, and duties in a professional and diligent manner in accordance with the following agreed terms:
{terms_clauses}

2. **Term and Termination:**
This Agreement shall commence on the Effective Date ({date_str}) and remain in full force and effect until complete performance of obligations or unless terminated earlier by mutual written agreement of both Parties or upon 15 days written notice for cause.

3. **Confidentiality and Proprietary Information:**
Each Party agrees to maintain the strict confidentiality of all proprietary, financial, or technical information received from the other Party during the term of this Agreement and for a period of two (2) years thereafter.

4. **Warranties and Limitation of Liability:**
Each Party warrants that its performance under this Agreement shall comply with all applicable regional and federal laws. Neither Party shall be liable for indirect, incidental, or consequential damages arising out of this Agreement.

5. **Governing Law and Dispute Resolution:**
This Agreement shall be interpreted and governed in accordance with the laws of the applicable governing jurisdiction. Any disputes arising hereunder shall first be submitted to good faith mediation before initiating formal legal proceedings.

6. **Severability and Entire Agreement:**
If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect. This Agreement constitutes the complete understanding between the Parties and supersedes all prior negotiations.

### IN WITNESS WHEREOF
The Parties have executed this {doc_title} as of the Effective Date written above.

________________________________________
**{party_a}**
Name: 
Title: 
Date: {date_str}

________________________________________
**{party_b}**
Name: 
Title: 
Date: {date_str}
"""
        return doc
