from typing import Dict, Any
import re

class LegalIssueClassifier:

    CATEGORIES = {
        "Cyber Crime": [
            "cyber", "hacking", "phishing", "online fraud", "identity theft",
            "ransomware", "malware", "internet crime"
        ],
        "Domestic Violence": [
            "domestic violence", "abuse", "spouse", "partner",
            "family violence", "physical assault", "emotional abuse"
        ],
        "Labour Dispute": [
            "labour", "employment", "worker", "salary", "wages",
            "job", "workplace", "union", "layoff", "termination", "company", "employer"
        ],
        "Consumer Complaint": [
            "consumer", "complaint", "refund", "product", "service",
            "warranty", "customer", "purchase", "seller"
        ],
        "Property Dispute": [
            "property", "land", "ownership", "title", "real estate",
            "boundary", "encroachment", "tenant", "lease"
        ]
    }

    DEFAULT_CATEGORY = "General Legal Issue"

    @classmethod
    def classify(cls, text: str) -> Dict[str, Any]:

        text_lower = text.lower()

        best_category = cls.DEFAULT_CATEGORY
        best_match_count = 0
        best_total_keywords = 1

        for category, keywords in cls.CATEGORIES.items():

            match_count = sum(
                1 for kw in keywords
                if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)
            )

            if match_count > best_match_count:
                best_category = category
                best_match_count = match_count
                best_total_keywords = len(keywords)

        confidence = best_match_count / best_total_keywords if best_match_count > 0 else 0.0

        return {
            "category": best_category,
            "confidence": round(confidence, 2)
        }
