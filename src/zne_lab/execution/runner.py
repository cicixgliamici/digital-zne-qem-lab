from __future__ import annotations

from dataclasses import dataclass

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel


@dataclass(frozen=True)
class ExecutionResult:
    """
    Result of a shot-based quantum circuit execution.
    """

    counts: dict[str, int]
    shots: int


def add_measurements(circuit: QuantumCircuit) -> QuantumCircuit:
    """
    Return a measured copy of the input circuit.

    The input circuit is expected to have no measurements.
    """
    measured = circuit.copy()
    measured.measure_all()
    return measured


def run_noisy_counts(
    circuit: QuantumCircuit,
    noise_model: NoiseModel,
    shots: int = 4096,
    seed: int = 42,
) -> ExecutionResult:
    """
    Execute a circuit on the Qiskit Aer noisy simulator and return counts.
    """
    measured = add_measurements(circuit)

    simulator = AerSimulator(
        noise_model=noise_model,
        seed_simulator=seed,
    )

    compiled = transpile(
        measured,
        simulator,
        seed_transpiler=seed,
    )

    job = simulator.run(compiled, shots=shots)
    result = job.result()
    counts = result.get_counts()

    return ExecutionResult(counts=counts, shots=shots)


def exact_zz_expectation(circuit: QuantumCircuit) -> float:
    """
    Compute the exact ideal expectation value of Z ⊗ Z.

    This function uses statevector simulation, so the input circuit must not
    contain measurements.
    """
    if circuit.num_qubits != 2:
        raise ValueError("exact_zz_expectation currently supports only 2 qubits.")

    state = Statevector.from_instruction(circuit)

    observable = SparsePauliOp.from_list([
        ("ZZ", 1.0),
    ])

    value = state.expectation_value(observable)

    return float(value.real)
