import pennylane as qml
from pennylane import numpy as np

def encode_sequence(sequence):
    """
    Encodes a genome sequence into a quantum-inspired state representation.
    Each nucleotide is mapped to a unique quantum state, with adjustments for purine-purine and purine-pyrimidine differences.
    """
    # Map nucleotides to angles (representing purine-purine and purine-pyrimidine relationships)
    mapping = {
        'A': 0.0,   # Purine
        'G': np.pi / 4,  # Purine
        'C': np.pi / 2,  # Pyrimidine
        'T': 3 * np.pi / 4  # Pyrimidine
    }

    purine = {'A', 'G'}
    pyrimidine = {'C', 'T'}

    encoded = []
    for i, nucleotide in enumerate(sequence):
        if nucleotide not in mapping:
            continue
        angle = mapping[nucleotide]
        if i > 0:  # Check the previous nucleotide for relationship
            prev_nucleotide = sequence[i - 1]
            if prev_nucleotide in purine and nucleotide in purine:
                angle *= 1.2  # Amplify purine-purine similarity
            elif (prev_nucleotide in purine and nucleotide in pyrimidine) or \
                 (prev_nucleotide in pyrimidine and nucleotide in purine):
                angle *= 0.8  # Reduce purine-pyrimidine similarity
        encoded.append(angle)

    return np.array(encoded)

def compute_superposition(angles):
    """
    Combines encoded angles into a quantum superposition vector.
    """
    n_qubits = 1
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        state = np.mean(angles)
        qml.RY(state, wires=0)
        return qml.state()

    return circuit()

def quantum_sequence_comparison(seq1, seq2):
    """
    Compares two genome sequences using the Quantum Sequence Representation method.
    Measures similarity using fidelity between quantum states.
    """
    # Encode sequences
    angles1 = encode_sequence(seq1)
    angles2 = encode_sequence(seq2)

    # Compute superposition vectors
    superposition1 = compute_superposition(angles1)
    superposition2 = compute_superposition(angles2)

    # Calculate fidelity between the quantum states
    fidelity = np.abs(np.dot(np.conj(superposition1), superposition2))**2
    return fidelity

# Example usage
if __name__ == "__main__":
    genome_sequence1 = input("Enter First Sequence")
    genome_sequence2 = input("Enter Second Sequence")

    similarity_score = quantum_sequence_comparison(genome_sequence1, genome_sequence2)
    print(f"Similarity Score between sequences: {similarity_score:.4f}")
