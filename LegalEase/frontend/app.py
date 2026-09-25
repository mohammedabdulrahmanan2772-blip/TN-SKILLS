import os
import sys
from pathlib import Path
import streamlit as st
import requests

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import INVERSE_LOGO_PATH, LOGO_PATH, BACKEND_URL
from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview
from ai_core.gemini_generator import GeminiDocumentGenerator

# Page Configuration
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling matching modern dark aesthetic
st.markdown("""
<style>
    /* Global background & text */
    .stApp {
        background-color: #0e1117;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Input widgets styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }
    
    /* Primary buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton>button:hover {
        background-color: #334155 !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
    }
    
    /* Document Preview Container */
    .doc-preview-card {
        background-color: #0b1120;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 24px 30px;
        margin: 18px 0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        max-height: 520px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #334155 #0b1120;
    }
    
    /* Subtitle header */
    .sub-header-title {
        text-align: center;
        font-size: 1.55rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.5px;
        margin-top: -8px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Sample Document Templates for Quick Demonstration
SAMPLE_PRESETS = {
    "-- Custom / Blank --": {
        "doc_type": "",
        "parties": "",
        "terms": "",
        "dates": ""
    },
    "Scenario 1: Freelance Work Contract": {
        "doc_type": "Freelance Work Contract",
        "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
        "terms": "Work must be delivered by May 15, 2025;\nPayment will be made within 7 days of invoice;\nClient retains intellectual property rights;\nConfidentiality must be maintained at all times;\nEither party may terminate with 15 days notice",
        "dates": "April 15, 2025"
    },
    "Scenario 2: Non-Disclosure Agreement (NDA)": {
        "doc_type": "Non-Disclosure Agreement (NDA)",
        "parties": "InnovateTech LLC (Disclosing Party), John Doe (Receiving Party)",
        "terms": "Recipient agrees not to disclose proprietary code, architecture, or business plans;\nObligations of confidentiality remain active for 3 years;\nInformation in public domain is excluded;\nInjunctive relief permitted upon breach",
        "dates": "May 01, 2025"
    },
    "Scenario 3: Residential Lease Agreement": {
        "doc_type": "Residential Lease Agreement",
        "parties": "XYZ Realty LLC (Landlord), Alice Smith (Tenant)",
        "terms": "Monthly rent of $2,200 due on the 1st of every month;\nSecurity deposit of $2,200 refundable within 14 days of move-out;\nNo unauthorized subletting or pets;\nLandlord provides 24 hours notice prior to maintenance entry",
        "dates": "June 01, 2025"
    },
    "Scenario 4: Employment Contract": {
        "doc_type": "Employment Contract",
        "parties": "Apex Solutions Inc. (Employer), Robert Johnson (Employee)",
        "terms": "Role of Senior Software Engineer with annual compensation of $140,000;\nStandard 40 hours per week with comprehensive health benefits;\n20 days paid annual leave;\nStrict non-compete clause for 12 months post-employment",
        "dates": "July 01, 2025"
    }
}

# Header layout with centered logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(INVERSE_LOGO_PATH):
        st.image(INVERSE_LOGO_PATH, use_container_width=True)
    elif os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center;'>⚖️ LegalEase</h1>", unsafe_allow_html=True)

st.markdown("<div class='sub-header-title'>AI Legal Document Generator</div>", unsafe_allow_html=True)

# Session state initialization
if "generated_text" not in st.session_state:
    st.session_state["generated_text"] = ""
if "show_edit" not in st.session_state:
    st.session_state["show_edit"] = False
if "doc_type" not in st.session_state:
    st.session_state["doc_type"] = "Freelance Work Contract"
if "parties" not in st.session_state:
    st.session_state["parties"] = "Jane Doe (Service Provider), TechNova Inc. (Client)"
if "terms" not in st.session_state:
    st.session_state["terms"] = "Work must be delivered by May 15, 2025;\nPayment will be made within 7 days of invoice;\nClient retains intellectual property rights;\nEither party may terminate with 15 days notice"
if "dates" not in st.session_state:
    st.session_state["dates"] = "April 15, 2025"

# Template Selector
selected_preset = st.selectbox(
    "💡 Load Template Preset (Optional):",
    options=list(SAMPLE_PRESETS.keys()),
    index=1
)

# If preset changed, update defaults
if selected_preset != "-- Custom / Blank --":
    preset_data = SAMPLE_PRESETS[selected_preset]
    default_doc_type = preset_data["doc_type"]
    default_parties = preset_data["parties"]
    default_terms = preset_data["terms"]
    default_dates = preset_data["dates"]
else:
    default_doc_type = ""
    default_parties = ""
    default_terms = ""
    default_dates = ""

# Form Inputs
with st.container():
    doc_type = st.text_input(
        "Document Type (Ex: Agreement, Contract, NDA)",
        value=default_doc_type,
        placeholder="e.g. Freelance Work Contract"
    )
    
    parties = st.text_area(
        "Parties Involved",
        value=default_parties,
        placeholder="e.g. Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=80
    )
    
    terms = st.text_area(
        "Terms & Conditions (Use semicolons for bullet points)",
        value=default_terms,
        placeholder="e.g. Payment to be made within 30 days of invoice; Confidentiality must be maintained at all times;",
        height=110
    )
    
    dates = st.text_input(
        "Effective Date",
        value=default_dates,
        placeholder="e.g. April 15, 2025"
    )

# Action button
if st.button("✨ Generate Document", use_container_width=True):
    if not doc_type.strip() or not parties.strip():
        st.warning("⚠️ Please provide at least the Document Type and Parties Involved.")
    else:
        with st.spinner("🤖 Drafting legal document with AI..."):
            payload = {
                "document_type": doc_type,
                "parties": parties,
                "terms": terms,
                "dates": dates
            }
            
            generated_doc = ""
            try:
                # Call FastAPI backend endpoint
                resp = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=30)
                if resp.status_code == 200:
                    generated_doc = resp.json().get("document", "")
                else:
                    # Fallback to direct generator if backend returned error
                    generator = GeminiDocumentGenerator()
                    generated_doc = generator.generate_document(doc_type, parties, terms, dates)
            except Exception:
                # Direct fallback in case backend is starting or offline
                generator = GeminiDocumentGenerator()
                generated_doc = generator.generate_document(doc_type, parties, terms, dates)
                
            if generated_doc:
                st.session_state["generated_text"] = sanitize_text(generated_doc)
                st.session_state["doc_type"] = doc_type
                st.session_state["show_edit"] = False
                st.success("✅ Document Generated Successfully!")
            else:
                st.error("❌ Failed to generate document. Please check inputs and try again.")

# Document Display, Edit & Export Section
if st.session_state.get("generated_text"):
    st.markdown("---")
    st.subheader("📜 Generated Legal Document")
    
    # Styled HTML Preview
    preview_html = format_html_preview(st.session_state["generated_text"])
    st.markdown(f"<div class='doc-preview-card'>{preview_html}</div>", unsafe_allow_html=True)
    
    # Edit toggle button
    edit_col1, edit_col2 = st.columns([1, 1])
    with edit_col1:
        if st.button("🖊️ " + ("Hide Editor" if st.session_state["show_edit"] else "Click to Edit Document"), use_container_width=True):
            st.session_state["show_edit"] = not st.session_state["show_edit"]
            st.rerun()
            
    # Editable Text Area
    if st.session_state.get("show_edit"):
        edited_text = st.text_area(
            "Edit Document Below:",
            value=st.session_state["generated_text"],
            height=320
        )
        if edited_text != st.session_state["generated_text"]:
            st.session_state["generated_text"] = sanitize_text(edited_text)
            
    # Multi-Format Download Options
    st.markdown("### 📥 Download Document")
    dcol1, dcol2, dcol3 = st.columns(3)
    
    current_text = st.session_state["generated_text"]
    current_doc_type = st.session_state.get("doc_type", "legal_document")
    file_slug = current_doc_type.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
    
    with dcol1:
        st.download_button(
            label="📄 Download as .TXT",
            data=current_text,
            file_name=f"{file_slug}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    with dcol2:
        try:
            docx_stream = format_docx(current_text, current_doc_type)
            st.download_button(
                label="📝 Download as .DOCX",
                data=docx_stream.getvalue(),
                file_name=f"{file_slug}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"DOCX error: {e}")
            
    with dcol3:
        try:
            pdf_stream = format_pdf(current_text, current_doc_type)
            st.download_button(
                label="📕 Download as .PDF",
                data=pdf_stream.getvalue(),
                file_name=f"{file_slug}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF error: {e}")
