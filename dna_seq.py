import re
from typing import List, Dict


# KMP ALGORITHM

def compute_lps(pattern: str) -> List[int]:
    """Compute LPS array for KMP."""
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search_all(text: str, pattern: str) -> List[int]:
    """
    KMP search for all occurrences of pattern in text.
    Returns list of start indices (0-based).
    """
    positions = []
    if not pattern:
        return positions

    lps = compute_lps(pattern)
    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                positions.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions


# dns seq and alignment
class DNASequence:
    """Represents a DNA sequence."""
    def __init__(self, name: str, sequence: str):
        self.name = name
        self.sequence = self.preprocess(sequence)

    def preprocess(self, seq: str) -> str:
        """Uppercase and remove invalid characters."""
        seq = seq.upper()
        seq = re.sub(r'[^ACGT]', '', seq)
        return seq

class KMPDNAAligner:
    """Align DNA motifs/patterns using KMP."""
    def __init__(self, motifs: Dict[str, str]):
        """
        motifs = {
            "TATA_box": "TATAAA",
            "promoter": "CAAT",
            "restriction_site": "GAATTC"
        }
        """
        self.motifs = {name: seq.upper() for name, seq in motifs.items()}

    def scan_sequence(self, dna_seq: DNASequence) -> Dict[str, List[int]]:
        """
        Returns a dictionary with motif names and positions they occur at.
        Example:
        { "TATA_box": [15, 102], "promoter": [] }
        """
        results = {}
        for name, pattern in self.motifs.items():
            positions = kmp_search_all(dna_seq.sequence, pattern)
            results[name] = positions
        return results

    def report_alignment(self, dna_seq: DNASequence):
        results = self.scan_sequence(dna_seq)
        print(f"\nDNA Sequence: {dna_seq.name}")
        print(f"Length: {len(dna_seq.sequence)}")
        print("--- Motif Scan Results ---")
        for motif, positions in results.items():
            if positions:
                pos_str = ", ".join(str(p + 1) for p in positions)  # 1-based index
                print(f"{motif}: Found at positions {pos_str}")
            else:
                print(f"{motif}: Not Found")


#user input
if __name__ == "__main__":
    # example DNA motifs
    motifs = {
        "TATA_box": "TATAAA",
        "CAAT_box": "GGCCAATCT",
        "EcoRI_site": "GAATTC"
    }

    print("\n--- KMP DNA Sequence Aligner ---\n")
    name = input("Enter DNA sequence name: ").strip()
    print("Enter DNA sequence (can include multiple lines, type END to finish):")
    seq_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        seq_lines.append(line.strip())
    sequence = "".join(seq_lines)

    dna = DNASequence(name, sequence)
    aligner = KMPDNAAligner(motifs)
    aligner.report_alignment(dna)
