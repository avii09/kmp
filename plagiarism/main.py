# KMP ALGORITHM IN USAGE

def build_lps(pattern):
    """
    Build Longest Prefix Suffix (LPS) array for KMP.
    lps[i] = length of the longest prefix of pattern
            that is also a suffix till index i
    """
    lps = [0] * len(pattern)
    j = 0  

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    return lps


def kmp_search(text, pattern):
    """
    KMP substring search.
    Returns True if pattern exists in text.
    """
    if not pattern:
        return False

    lps = build_lps(pattern)
    i = j = 0  

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == len(pattern):
            return True  

        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False

# PLAGIARISM DETECTION USING KMP
def find_plagiarism(doc1, doc2, min_length=10):
    """
    Uses KMP to find matching phrases between two documents.
    min_length: number of words to treat as a phrase.
    """
    matches = []

    words1 = doc1.split()
    words2 = doc2.split()
    full_doc2 = " ".join(words2)

    for i in range(len(words1) - min_length + 1):
        phrase = " ".join(words1[i:i + min_length])
        if kmp_search(full_doc2, phrase):
            matches.append(phrase)

    return matches



# LOAD DOCUMENTS AND RUN PROGRAM

def load_documents():
    # with open("doc1.txt", "r") as f:
    with open("doc1_plagiarized.txt", "r") as f:
        doc_a = f.read()

    # with open("doc2.txt", "r") as f:
    with open("doc2_plagiarized.txt", "r") as f:
        doc_b = f.read()

    return doc_a, doc_b


if __name__ == "__main__":
    doc_a, doc_b = load_documents()

    min_length = 5  
    matches = find_plagiarism(doc_a, doc_b, min_length)

    print("\n--- PLAGIARISM REPORT ---\n")

    if matches:
        print("Possible plagiarised segments found:\n")
        for m in matches:
            print(" •", m)
    else:
        print("No plagiarism detected.")
