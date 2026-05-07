from qiskit import QuantumCircuit


def build_ghz_circuit(num_qubits: int = 3) -> QuantumCircuit:
    """
    Build a GHZ-state preparation circuit.

    The ideal final state is:

        (|00...0> + |11...1>) / sqrt(2)

    This is not used in MVP 0, but it is useful for MVP 1.
    """
    if num_qubits < 2:
        raise ValueError("A GHZ circuit requires at least 2 qubits.")

    circuit = QuantumCircuit(num_qubits, name=f"ghz_{num_qubits}")
    circuit.h(0)

    for target in range(1, num_qubits):
        circuit.cx(0, target)

    return circuit
