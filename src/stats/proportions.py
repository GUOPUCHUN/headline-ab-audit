"""Two-proportion tests, confidence intervals and power for CTR comparisons."""

from dataclasses import dataclass

import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest


@dataclass(frozen=True)
class ProportionTestResult:
    ctr_a: float
    ctr_b: float
    diff: float
    relative_lift: float
    z_stat: float
    p_value: float
    ci_low: float
    ci_high: float


def two_proportion_test(
    x_a: int, n_a: int, x_b: int, n_b: int, alpha: float = 0.05
) -> ProportionTestResult:
    """Compare arm B with arm A: difference, z-test and Wald confidence interval."""
    if n_a <= 0 or n_b <= 0:
        raise ValueError("Impressions must be positive.")
    ctr_a, ctr_b = x_a / n_a, x_b / n_b
    z_stat, p_value = proportions_ztest([x_b, x_a], [n_b, n_a])
    ci_low, ci_high = confint_proportions_2indep(
        x_b, n_b, x_a, n_a, compare="diff", method="wald", alpha=alpha
    )
    diff = ctr_b - ctr_a
    return ProportionTestResult(
        ctr_a=ctr_a,
        ctr_b=ctr_b,
        diff=diff,
        relative_lift=diff / ctr_a if ctr_a > 0 else float("nan"),
        z_stat=float(z_stat),
        p_value=float(p_value),
        ci_low=float(ci_low),
        ci_high=float(ci_high),
    )


def _z_values(alpha: float, power: float) -> tuple[float, float]:
    return stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)


def minimum_detectable_effect(
    baseline_ctr: float, n_a: int, n_b: int, alpha: float = 0.05, power: float = 0.8
) -> float:
    """Smallest absolute CTR difference detectable with the given sample sizes."""
    z_alpha, z_beta = _z_values(alpha, power)
    variance = baseline_ctr * (1 - baseline_ctr) * (1 / n_a + 1 / n_b)
    return float((z_alpha + z_beta) * np.sqrt(variance))


def sample_size_per_arm(
    baseline_ctr: float, relative_lift: float, alpha: float = 0.05, power: float = 0.8
) -> float:
    """Impressions per arm needed to detect a relative lift in CTR."""
    z_alpha, z_beta = _z_values(alpha, power)
    absolute = relative_lift * baseline_ctr
    return float((z_alpha + z_beta) ** 2 * 2 * baseline_ctr * (1 - baseline_ctr) / absolute**2)