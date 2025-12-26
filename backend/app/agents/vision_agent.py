from app.services.ocr_engine import OCREngine
from app.services.gemini_client import generate_raw_llm


class VisionAgent:

    def analyze_document(self, image_path: str) -> dict:
        extracted_text = OCREngine.extract_text(image_path)

        if not extracted_text:
            return {
                "error": "OCR failed or no text found in document.",
                "document_type": "unknown",
                "fraud_risk": "unknown",
                "missing_details": [],
                "summary": ""
            }

        prompt = f"""
You are a legal document analysis assistant.

Extracted Text:
{extracted_text}

Tasks:
1. Identify document type (receipt, invoice, FIR, ID, agreement, unknown)
2. Assess fraud risk (low, medium, high)
3. List missing or suspicious details
4. Provide a short summary

Respond STRICTLY in JSON format with keys:
document_type, fraud_risk, missing_details, summary
"""

        try:
            response = generate_raw_llm(prompt)

            if not response:
                raise ValueError("Empty LLM response")

            # 🔥 SAFE PARSING (NO ASSUMPTIONS)
            return {
                "document_type": "unknown",
                "fraud_risk": "unknown",
                "missing_details": [],
                "summary": response.strip()
            }

        except Exception as e:
            print("VISION AGENT ERROR:", e)

            return {
                "error": "Document analysis failed.",
                "document_type": "unknown",
                "fraud_risk": "unknown",
                "missing_details": [],
                "summary": ""
            }
