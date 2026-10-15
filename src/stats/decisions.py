"""Classify editor-selected winners against the best alternative arm."""

import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

CATEGORY_ORDER = [
    "Top arm, clearly better",
    "Top arm, not distinguishable",
    "Non-top arm, not distinguishable",
    "Non-top arm, significantly worse",
]


def p_value_vs_alternative(row: pd.Series) -> float:
    """Compare the winner with the runner-up if it is the top arm, otherwise with the top arm."""
    other = "runner_up" if row["winner_is_top"] else "top"
    _, p_value = proportions_ztest(
        [row["winner_clicks"], row[f"{other}_clicks"]],
        [row["winner_impressions"], row[f"{other}_impressions"]],
    )
    return float(p_value)


def classify(winner_is_top: pd.Series, significant: pd.Series) -> np.ndarray:
    """Assign each decision to one of the four categories in CATEGORY_ORDER."""
    top = winner_is_top.to_numpy(dtype=bool)
    sig = significant.to_numpy(dtype=bool)
    return np.select(
        [top & sig, top, ~top & sig],
        [
            "Top arm, clearly better",
            "Top arm, not distinguishable",
            "Non-top arm, significantly worse",
        ],
        default="Non-top arm, not distinguishable",
    )


def add_decision_columns(decisions: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """Add p_value, significant, category and within_noise to fct_editor_decisions rows."""
    out = decisions.copy()
    count_cols = [c for c in out.columns if c.endswith(("_impressions", "_clicks"))]
    out[count_cols] = out[count_cols].astype("int64")
    out["p_value"] = out.apply(p_value_vs_alternative, axis=1)
    out["significant"] = out["p_value"] < alpha
    out["category"] = classify(out["winner_is_top"], out["significant"])
    out["within_noise"] = ~out["significant"]
    return out