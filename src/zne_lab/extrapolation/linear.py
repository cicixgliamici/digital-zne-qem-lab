from __future__ import annotations

import numpy as np


def linear_zero_noise_extrapolation(
    scale_factors: list[float],
    expectation_values: list[float],
) -> float:
    """
    Perform linear zero-noise extrapolation.

    We fit:

        E(s) = a s + b

    where:
    - s is the noise scale factor;
    - E(s) is the measured expectation value.

    The zero-noise estimate is:

        E(0) = b
    """
    if len(scale_factors) != len(expectation_values):
        raise ValueError("scale_factors and expectation_values must have the same length.")

    if len(scale_factors) < 2:
        raise ValueError("At least two points are required for linear extrapolation.")

    coefficients = np.polyfit(scale_factors, expectation_values, deg=1)

    slope = coefficients[0]
    intercept = coefficients[1]

    return float(intercept)
