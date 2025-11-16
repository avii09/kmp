import re
from typing import List, Dict



# KMP ALGORITHM
def compute_lps(pattern: str) -> List[int]:
    """compute LPS array"""
    lps = [0] * len(pattern)
    prefix = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[prefix]:
            prefix += 1
            lps[i] = prefix
            i += 1
        else:
            if prefix != 0:
                prefix = lps[prefix - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str) -> bool:
    """run KMP search and return true if pattern exists in text."""
    if not pattern:
        return False

    lps = compute_lps(pattern)
    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return True
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False



#email and spam filteree
class Email:
    def __init__(self, sender: str, subject: str, body: str):
        self.sender = sender
        self.subject = subject
        self.body = body

    def full_text(self) -> str:
        return (self.subject + " " + self.body).lower()


class KMPSpamFilter:
    def __init__(self, rules: Dict[str, List[str]]):
        self.rules = rules

    def preprocess(self, text: str) -> str:
        """
        normalize spaces,
        keep punctuation in URLs, filenames, hyphens
        """
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)  # normalize spaces
        return text

    def scan_email(self, email: Email) -> Dict[str, bool]:
        clean_text = self.preprocess(email.full_text())
        results = {}
        for category, patterns in self.rules.items():
            results[category] = any(
                kmp_search(clean_text, p.lower()) for p in patterns
            )
        return results

    def is_spam(self, email: Email) -> bool:
        category_hits = self.scan_email(email)
        return any(category_hits.values())



#user input (sneder, subject, body of emal)
if __name__ == "__main__":
    # spam rule categories
    spam_rules = {
        "financial_spam": [
            "win money", "claim your prize", "free cash", "lottery winner"
        ],
        "phishing": [
            "verify your account", "verify your account immediately",
            "confirm your identity", "update your password",
            "login to avoid suspension"
        ],
        "malware": [
            "download attachment", "download the attached file",
            "install this file", "run this program", "open the attached file"
        ]
    }

    print("\n--- KMP-Based Spam Filter ---\n")

    sender = input("Enter sender email: ").strip()
    subject = input("Enter email subject: ").strip()

    print("\nEnter email body (type END on a new line to finish):")
    body_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)

    email = Email(sender, subject, body)

    filter = KMPSpamFilter(spam_rules)
    results = filter.scan_email(email)

    print("\n--- Spam Scan Results ---")
    for category, value in results.items():
        print(f"{category}: {'Detected' if value else 'Not Detected'}")

    print("\nFinal Decision:", "SPAM" if filter.is_spam(email) else "NOT SPAM")