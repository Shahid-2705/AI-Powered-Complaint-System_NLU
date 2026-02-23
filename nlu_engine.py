import torch
from transformers import pipeline


class SmartIncidentNLU:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Loading models on device {'GPU' if self.device >= 0 else 'CPU'}...")

        # Zero-shot classifier
        self.classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",
            device=self.device
        )

        # Sentiment analyzer
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            device=self.device
        )

        # Reply generator
        self.reply_generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            device=self.device
        )

        # Detailed labels for zero-shot fallback
        self.detailed_categories = [
            "Delivery delay issue related to late or missing shipment",
            "Payment issue related to transaction or billing problem",
            "Technical problem related to website, app, or system malfunction",
            "Refund request for cancelled or returned order",
            "General inquiry or information request"
        ]

        self.dept_mapping = {
            "Delivery Delay": "Logistics",
            "Payment Issue": "Finance",
            "Technical Problem": "IT Support",
            "Refund Request": "Accounts",
            "General Inquiry": "Customer Care"
        }

        self.sentiment_mapping = {
            "LABEL_0": "Negative",
            "LABEL_1": "Neutral",
            "LABEL_2": "Positive"
        }

    # =====================================================
    def analyze_complaint(self, text):

        text_lower = text.lower()

        # --------------------------------------------------
        # 1️⃣ CATEGORY DETECTION (Hybrid Rule + Zero-shot)
        # --------------------------------------------------
        if any(word in text_lower for word in ["deliver", "shipment", "courier", "not arrived", "hasn't arrived"]):
            predicted_category = "Delivery Delay"

        elif any(word in text_lower for word in ["payment", "charged", "deducted", "billing"]):
            predicted_category = "Payment Issue"

        elif any(word in text_lower for word in ["refund", "return money"]):
            predicted_category = "Refund Request"

        elif any(word in text_lower for word in ["crash", "error", "bug", "not working", "website"]):
            predicted_category = "Technical Problem"

        else:
            cat_result = self.classifier(
                text,
                candidate_labels=self.detailed_categories,
                multi_label=False
            )

            top_label = cat_result["labels"][0]

            if "Delivery delay" in top_label:
                predicted_category = "Delivery Delay"
            elif "Payment issue" in top_label:
                predicted_category = "Payment Issue"
            elif "Technical problem" in top_label:
                predicted_category = "Technical Problem"
            elif "Refund request" in top_label:
                predicted_category = "Refund Request"
            else:
                predicted_category = "General Inquiry"

        # --------------------------------------------------
        # 2️⃣ SENTIMENT
        # --------------------------------------------------
        sent_result = self.sentiment_analyzer(text)[0]
        mapped_sentiment = self.sentiment_mapping.get(
            sent_result["label"], "Neutral"
        )

        # --------------------------------------------------
        # 3️⃣ PRIORITY LOGIC (Improved)
        # --------------------------------------------------
        high_priority_keywords = [
            "not delivered",
            "hasn't been delivered",
            "no update",
            "no response",
            "urgent",
            "immediately",
            "delay",
            "still waiting",
            "fraud",
            "worst",
            "complaint",
            "refund not received",
            "very frustrating"
        ]

        if mapped_sentiment == "Negative":
            if any(word in text_lower for word in high_priority_keywords):
                predicted_priority = "High"
            else:
                predicted_priority = "Medium"
        else:
            predicted_priority = "Low"

        # --------------------------------------------------
        # 4️⃣ ROUTING
        # --------------------------------------------------
        department = self.dept_mapping.get(
            predicted_category,
            "Customer Care"
        )

        # --------------------------------------------------
        # 5️⃣ ESCALATION
        # --------------------------------------------------
        escalation_keywords = ["legal", "court", "police", "fraud"]

        if (
            predicted_priority == "High"
            and mapped_sentiment == "Negative"
        ) or any(word in text_lower for word in escalation_keywords):
            escalation_flag = True
        else:
            escalation_flag = False

        # --------------------------------------------------
        # 6️⃣ AUTO REPLY (Clean & Controlled)
        # --------------------------------------------------
        prompt = f"""
You are a professional customer support representative.

Customer complaint:
{text}

Write a short, empathetic and professional reply.
Apologize for the inconvenience.
Reassure the customer that the issue is being investigated.
Keep it under 3 sentences.
"""

        reply_result = self.reply_generator(
            prompt,
            max_length=70,
            do_sample=False,
            repetition_penalty=1.8,
            no_repeat_ngram_size=3
        )

        auto_reply = reply_result[0]["generated_text"].strip()

        # --------------------------------------------------
        return {
            "complaint_text": text,
            "category": predicted_category,
            "sentiment": mapped_sentiment,
            "priority": predicted_priority,
            "department": department,
            "escalation_flag": escalation_flag,
            "reply_text": auto_reply
        }


# =====================================================
# LOCAL TEST
# =====================================================
if __name__ == "__main__":
    nlu = SmartIncidentNLU()

    sample = "I ordered a mobile phone 6 days ago and it still hasn't been delivered. No updates from your side. This is very frustrating."

    print("\nTesting Sample Complaint:\n")

    result = nlu.analyze_complaint(sample)

    for key, value in result.items():
        print(f"{key}: {value}")