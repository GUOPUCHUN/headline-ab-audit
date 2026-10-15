"""Sample ratio mismatch (SRM) checks for headline tests."""

import numpy as np
import pandas as pd
from scipy import stats

SRM_ALPHA = 0.001
WINDOW_START = pd.Timestamp("2013-06-25")
WINDOW_END = pd.Timestamp("2014-01-10 23:59:59")


def chi_square_stat(observed) -> float:
    """Chi-square statistic for impressions under equal allocation across arms."""
    counts = np.asarray(observed, dtype=float)
    if counts.size < 2:
        raise ValueError("At least two arms are needed.")
    total = counts.sum()
    if total <= 0:
        raise ValueError("Total impressions must be positive.")
    expected = total / counts.size
    return float(((counts - expected) ** 2 / expected).sum())


def srm_p_value(chi_square, degrees_of_freedom):
    """P-value of the chi-square statistic. Works on scalars and pandas Series."""
    return stats.chi2.sf(chi_square, degrees_of_freedom)


def assign_period(started_at: pd.Series) -> np.ndarray:
    """Label tests as before, inside, or after the window flagged by the archive authors."""
    return np.select(
        [started_at < WINDOW_START, started_at <= WINDOW_END],
        ["before window", "flagged window"],
        default="after window",
    )


def add_srm_columns(balance: pd.DataFrame, alpha: float = SRM_ALPHA) -> pd.DataFrame:
    """Add p_srm, is_srm and period to rows of fct_test_balance."""
    out = balance.copy()
    out["p_srm"] = srm_p_value(out["chi_square_stat"], out["degrees_of_freedom"])
    out["is_srm"] = out["p_srm"] < alpha
    out["period"] = assign_period(out["started_at"])
    return out


def reliable_test_ids(balance: pd.DataFrame, period: str = "after window") -> set[str]:
    """Tests in the given period that pass the SRM check (the Q1 decision)."""
    checked = add_srm_columns(balance)
    mask = (checked["period"] == period) & ~checked["is_srm"]
    return set(checked.loc[mask, "test_id"])