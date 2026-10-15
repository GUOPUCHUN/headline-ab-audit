import pandas as pd

from src.stats.decisions import add_decision_columns, classify


def test_classify_covers_all_four_categories():
    winner_is_top = pd.Series([True, True, False, False])
    significant = pd.Series([True, False, True, False])
    assert list(classify(winner_is_top, significant)) == [
        "Top arm, clearly better",
        "Top arm, not distinguishable",
        "Non-top arm, significantly worse",
        "Non-top arm, not distinguishable",
    ]


def test_add_decision_columns_compares_with_the_right_arm():
    decisions = pd.DataFrame(
        {
            "winner_is_top": [True, False],
            "winner_clicks": [300, 100],
            "winner_impressions": [10000, 10000],
            "top_clicks": [300, 300],
            "top_impressions": [10000, 10000],
            "runner_up_clicks": [290, 100],
            "runner_up_impressions": [10000, 10000],
        }
    )
    result = add_decision_columns(decisions)
    assert list(result["category"]) == [
        "Top arm, not distinguishable",
        "Non-top arm, significantly worse",
    ]