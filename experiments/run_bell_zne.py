from __future__ import annotations

import csv
from pathlib import Path

from zne_lab.circuits.bell import build_bell_circuit
from zne_lab.noise.depolarizing import build_depolarizing_noise_model
from zne_lab.folding.global_folding import global_fold
from zne_lab.execution.runner import run_noisy_counts, exact_zz_expectation
from zne_lab.evaluation.metrics import (
    zz_expectation_from_counts,
    absolute_error,
    relative_improvement,
)
from zne_lab.extrapolation.linear import linear_zero_noise_extrapolation


def main() -> None:
    shots = 4096
    seed = 42

    scale_factors = [1, 3, 5]

    single_qubit_error_rate = 0.001
    two_qubit_error_rate = 0.01

    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "bell_zne_results.csv"

    base_circuit = build_bell_circuit()

    ideal_expectation = exact_zz_expectation(base_circuit)

    noise_model = build_depolarizing_noise_model(
        single_qubit_error_rate=single_qubit_error_rate,
        two_qubit_error_rate=two_qubit_error_rate,
    )

    expectation_values: list[float] = []
    rows: list[dict[str, float | int]] = []

    print()
    print("Digital Zero-Noise Extrapolation — Bell Circuit MVP 0")
    print("=" * 64)
    print(f"Shots:                   {shots}")
    print(f"Single-qubit error rate: {single_qubit_error_rate}")
    print(f"Two-qubit error rate:    {two_qubit_error_rate}")
    print(f"Ideal <ZZ>:              {ideal_expectation:.6f}")
    print()

    for scale_factor in scale_factors:
        folded_circuit = global_fold(base_circuit, scale_factor)

        result = run_noisy_counts(
            folded_circuit,
            noise_model=noise_model,
            shots=shots,
            seed=seed,
        )

        expectation = zz_expectation_from_counts(result.counts)
        expectation_values.append(expectation)

        error = absolute_error(expectation, ideal_expectation)

        rows.append({
            "scale_factor": scale_factor,
            "expectation_zz": expectation,
            "absolute_error": error,
            "shots": shots,
        })

        print(
            f"scale_factor={scale_factor:<2} "
            f"<ZZ>={expectation:.6f} "
            f"abs_error={error:.6f}"
        )

    raw_noisy_estimate = expectation_values[0]

    zne_estimate = linear_zero_noise_extrapolation(
        scale_factors=[float(x) for x in scale_factors],
        expectation_values=expectation_values,
    )

    raw_error = absolute_error(raw_noisy_estimate, ideal_expectation)
    zne_error = absolute_error(zne_estimate, ideal_expectation)
    improvement = relative_improvement(raw_error, zne_error)

    print()
    print("Summary")
    print("-" * 64)
    print(f"Ideal expectation:      {ideal_expectation:.6f}")
    print(f"Raw noisy expectation:  {raw_noisy_estimate:.6f}")
    print(f"ZNE expectation:        {zne_estimate:.6f}")
    print(f"Raw absolute error:     {raw_error:.6f}")
    print(f"ZNE absolute error:     {zne_error:.6f}")
    print(f"Relative improvement:   {improvement:.2f}%")

    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "scale_factor",
                "expectation_zz",
                "absolute_error",
                "shots",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Saved results to: {output_file}")


if __name__ == "__main__":
    main()
