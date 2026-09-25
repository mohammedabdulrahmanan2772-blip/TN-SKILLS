import io
import os
import re
from typing import Optional
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from fpdf import FPDF
from config import LOGO_PATH

def sanitize_text(text: str) -> str:
    """
    Sanitize text to remove/normalize typographic quotes and special characters
    ensuring clean cross-platform formatting for DOCX, PDF, and HTML.
    """
    if not text:
        return ""
    
    replacements = {
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '—': ' - ',
        '–': ' - ',
        '…': '...',
        '\u200b': '',  # zero-width space
        '\xa0': ' ',   # non-breaking space
        '\r\n': '\n',
        '\r': '\n'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.strip()

def format_html_preview(text: str) -> str:
    """
    Converts legal markdown/text into stylized dark-themed HTML preview blocks.
    """
    if not text:
        return "<p><em>No document content generated yet.</em></p>"
    
    cleaned = sanitize_text(text)
    lines = cleaned.split("\n")
    html_parts = []
    
    in_list = False
    
    for line in lines:
        line_str = line.strip()
        if not line_str:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("<div style='height: 10px;'></div>")
            continue
        
        # Heading 1 (#)
        if line_str.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            title = line_str[2:].strip()
            html_parts.append(f"<h2 style='color: #60a5fa; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-top: 15px; margin-bottom: 12px; font-weight: 700; letter-spacing: 0.5px;'>{title}</h2>")
        # Heading 2 (##)
        elif line_str.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            title = line_str[3:].strip()
            html_parts.append(f"<h3 style='color: #93c5fd; margin-top: 14px; margin-bottom: 8px; font-weight: 600;'>{title}</h3>")
        # Heading 3 (###)
        elif line_str.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            title = line_str[4:].strip()
            html_parts.append(f"<h4 style='color: #bfdbfe; margin-top: 12px; margin-bottom: 6px; font-weight: 600;'>{title}</h4>")
        # Numbered section headers like "1. Services:" or "1. Term and Termination"
        elif re.match(r"^\d+\.\s+.*:", line_str) or (re.match(r"^\d+\.\s+", line_str) and len(line_str) < 60):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<div style='font-size: 1.05rem; font-weight: 700; color: #38bdf8; margin-top: 12px; margin-bottom: 4px;'>{line_str}</div>")
        # Bullet list items (* or -)
        elif line_str.startswith(("* ", "- ", "• ")):
            if not in_list:
                html_parts.append("<ul style='margin-left: 20px; color: #e2e8f0; line-height: 1.6;'>")
                in_list = True
            content = line_str[2:].strip()
            # bold parser inside bullet
            content = re.sub(r"\*\*(.*?)\*\*", r"<strong style='color: #ffffff;'>\1</strong>", content)
            html_parts.append(f"<li style='margin-bottom: 6px;'>{content}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            
            # Formatted normal paragraph
            content = line_str
            content = re.sub(r"\*\*(.*?)\*\*", r"<strong style='color: #ffffff;'>\1</strong>", content)
            
            if content.upper() in ["WITNESSETH:", "NOW, THEREFORE,", "IN WITNESS WHEREOF,"]:
                html_parts.append(f"<p style='font-weight: bold; color: #cbd5e1; letter-spacing: 1px; margin: 12px 0 6px 0; text-transform: uppercase;'>{content}</p>")
            elif "Between:" in content or "And:" in content:
                html_parts.append(f"<p style='font-weight: 600; color: #94a3b8; margin: 10px 0 4px 0;'>{content}</p>")
            else:
                html_parts.append(f"<p style='color: #cbd5e1; line-height: 1.65; margin-bottom: 8px;'>{content}</p>")
                
    if in_list:
        html_parts.append("</ul>")
        
    return "".join(html_parts)

def format_docx(text: str, doc_type: str, logo_path: Optional[str] = None) -> io.BytesIO:
    """
    Format AI legal document into structured Microsoft Word .docx format.
    Includes logo, Times New Roman typography, styled headings, terms table, and legal footer.
    """
    doc = Document()
    
    # Page Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("LegalEase Inc. | contact@legalease.com | All Rights Reserved.")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(9)
        f_run.font.color.rgb = RGBColor(128, 128, 128)
    
    # Add Logo if available
    logo_file = logo_path or LOGO_PATH
    if os.path.exists(logo_file):
        try:
            logo_p = doc.add_paragraph()
            logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            logo_run = logo_p.add_run()
            logo_run.add_picture(logo_file, width=Inches(2.5))
            logo_p.paragraph_format.space_after = Pt(12)
        except Exception as e:
            print(f"Error adding logo to docx: {e}")
    
    # Document Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(doc_type.upper() if doc_type else "LEGAL AGREEMENT")
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)
    title_p.paragraph_format.space_after = Pt(18)
    
    cleaned_text = sanitize_text(text)
    lines = cleaned_text.split("\n")
    
    terms_list = []
    in_terms_collection = False
    
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        # Detect Headings
        if line_clean.startswith("# ") or line_clean.startswith("## ") or line_clean.startswith("### "):
            header_text = line_clean.lstrip("#").strip()
            # Check if this is the duplicate main title
            if header_text.lower() == doc_type.lower():
                continue
            h_p = doc.add_paragraph()
            h_p.paragraph_format.space_before = Pt(12)
            h_p.paragraph_format.space_after = Pt(4)
            h_run = h_p.add_run(header_text)
            h_run.font.name = "Times New Roman"
            h_run.font.size = Pt(13)
            h_run.font.bold = True
            h_run.font.color.rgb = RGBColor(30, 41, 59)
            
        # Numbered Sections (e.g., 1. Services:, 2. Term and Termination:)
        elif re.match(r"^\d+\.\s+", line_clean):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            
            # Split section title from body if on same line
            match = re.match(r"^(\d+\.\s+[^:]+:?)(.*)", line_clean)
            if match:
                sec_title, sec_body = match.groups()
                r1 = p.add_run(sec_title)
                r1.font.name = "Times New Roman"
                r1.font.size = Pt(11)
                r1.font.bold = True
                
                if sec_body.strip():
                    r2 = p.add_run(sec_body)
                    r2.font.name = "Times New Roman"
                    r2.font.size = Pt(11)
            else:
                r = p.add_run(line_clean)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                r.font.bold = True
                
        # Bullet list items
        elif line_clean.startswith(("* ", "- ", "• ")):
            bullet_text = line_clean[2:].strip()
            # Clean markdown bold markers
            bullet_text_clean = bullet_text.replace("**", "")
            
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(bullet_text_clean)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            
        else:
            # Regular paragraph
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            
            # Check for signature blocks or bold phrases
            clean_p_text = line_clean.replace("**", "")
            r = p.add_run(clean_p_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            
            if clean_p_text.upper() in ["WITNESSETH:", "NOW, THEREFORE,", "IN WITNESS WHEREOF,"]:
                r.font.bold = True
                p.paragraph_format.space_before = Pt(8)
    
    # Save to BytesIO buffer
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)
    return output_stream

class LegalPDF(FPDF):
    def __init__(self, doc_type: str, logo_path: Optional[str] = None):
        super().__init__()
        self.doc_type = doc_type
        self.logo_path = logo_path or LOGO_PATH
        self.set_auto_page_break(auto=True, margin=25)
        
    def header(self):
        # Center-aligned Logo on page header
        if os.path.exists(self.logo_path):
            try:
                # 210mm page width, 60mm image width -> center is (210-60)/2 = 75
                self.image(self.logo_path, x=75, y=10, w=60)
                self.ln(22)
            except Exception:
                self.ln(5)
        else:
            self.ln(5)
            
    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        # Legal footer text
        self.cell(0, 5, "LegalEase Inc. | contact@legalease.com | All Rights Reserved.", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

def format_pdf(text: str, doc_type: str, logo_path: Optional[str] = None) -> io.BytesIO:
    """
    Format AI legal document into clean, branded PDF with logo, bold headings,
    bullet-style terms, and footer on all pages.
    """
    pdf = LegalPDF(doc_type=doc_type, logo_path=logo_path)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, doc_type.upper() if doc_type else "LEGAL AGREEMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    cleaned_text = sanitize_text(text)
    lines = cleaned_text.split("\n")
    
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            pdf.ln(3)
            continue
            
        # Heading 1, 2, 3
        if line_clean.startswith("# ") or line_clean.startswith("## ") or line_clean.startswith("### "):
            header_text = line_clean.lstrip("#").strip()
            if header_text.lower() == doc_type.lower():
                continue
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 6, header_text)
            pdf.ln(2)
            
        # Numbered Section headings
        elif re.match(r"^\d+\.\s+", line_clean):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.set_text_color(15, 23, 42)
            
            clean_str = line_clean.replace("**", "")
            pdf.multi_cell(0, 5.5, clean_str)
            pdf.ln(1)
            
        # Bullet Points
        elif line_clean.startswith(("* ", "- ", "• ")):
            bullet_content = line_clean[2:].strip().replace("**", "")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            
            # Draw indent bullet
            pdf.set_x(pdf.get_x() + 5)
            pdf.multi_cell(0, 5, f"- {bullet_content}")
            pdf.ln(1)
            
        else:
            clean_body = line_clean.replace("**", "")
            
            if clean_body.upper() in ["WITNESSETH:", "NOW, THEREFORE,", "IN WITNESS WHEREOF,"]:
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(30, 41, 59)
                pdf.multi_cell(0, 5, clean_body)
                pdf.ln(1)
            else:
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(30, 41, 59)
                pdf.multi_cell(0, 5.5, clean_body)
                pdf.ln(1.5)
                
    pdf_bytes = pdf.output()
    return io.BytesIO(pdf_bytes)
