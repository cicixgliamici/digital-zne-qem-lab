from qiskit_aer.noise import NoiseModel, depolarizing_error


def build_depolarizing_noise_model(
    single_qubit_error_rate: float = 0.001,
    two_qubit_error_rate: float = 0.01,
) -> NoiseModel:
    """
    Build a simple depolarizing noise model.

    We attach:
    - single-qubit depolarizing noise to H/X/SX gates;
    - two-qubit depolarizing noise to CX gates.

    This is intentionally simple for MVP 0.
    """
    if not 0.0 <= single_qubit_error_rate <= 1.0:
        raise ValueError("single_qubit_error_rate must be in [0, 1].")

    if not 0.0 <= two_qubit_error_rate <= 1.0:
        raise ValueError("two_qubit_error_rate must be in [0, 1].")

    noise_model = NoiseModel()

    single_qubit_error = depolarizing_error(single_qubit_error_rate, 1)
    two_qubit_error = depolarizing_error(two_qubit_error_rate, 2)

    noise_model.add_all_qubit_quantum_error(
        single_qubit_error,
        ["h", "x", "sx"],
    )

    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx"],
    )

    return noise_model
