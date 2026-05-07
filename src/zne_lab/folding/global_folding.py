from qiskit import QuantumCircuit


def global_fold(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Apply global unitary folding.

    For odd scale factors:

        scale_factor = 1:
            U

        scale_factor = 3:
            U U† U

        scale_factor = 5:
            U U† U U† U

    In the ideal noiseless case, this preserves the same unitary semantics,
    because U U† = I.

    In the noisy case, the circuit becomes longer and experiences more noise.
    """
    if scale_factor < 1:
        raise ValueError("scale_factor must be >= 1.")

    if scale_factor % 2 == 0:
        raise ValueError("Only odd scale factors are supported in MVP 0.")

    folded = QuantumCircuit(circuit.num_qubits, name=f"{circuit.name}_fold_{scale_factor}")

    folded.compose(circuit, inplace=True)

    repetitions = (scale_factor - 1) // 2

    for _ in range(repetitions):
        folded.compose(circuit.inverse(), inplace=True)
        folded.compose(circuit, inplace=True)

    return folded
