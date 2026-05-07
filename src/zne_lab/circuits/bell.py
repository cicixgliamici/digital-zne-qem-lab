from qiskit import QuantumCircuit


def build_bell_circuit() -> QuantumCircuit:
    """
    Build a Bell-state preparation circuit.

    The ideal final state is:

        |Φ+> = (|00> + |11>) / sqrt(2)

    For this state, the expectation value of Z ⊗ Z is +1.
    """
    circuit = QuantumCircuit(2, name="bell")
    circuit.h(0)
    circuit.cx(0, 1)
    return circuit
