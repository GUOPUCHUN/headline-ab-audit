import pandas as pd
import pytest
from scipy import stats

from src.stats.srm import assign_period, chi_square_stat, reliable_test_ids, srm_p_value


def test_chi_square_stat_is_zero_for_equal_arms():
    assert chi_square_stat([100, 100, 100]) == 0.0


def test_chi_square_stat_matches_scipy():
    observed = [120, 95, 105, 80]
    expected = stats.chisquare(observed).statistic
    assert chi_square_stat(observed) == pytest.approx(expected)


@pytest.mark.parametrize("observed", [[100], [0, 0]])
def test_chi_square_stat_rejects_invalid_input(observed):
    with pytest.raises(ValueError):
        chi_square_stat(observed)


def test_srm_p_value_bounds():
    assert srm_p_value(0.0, 3) == pytest.approx(1.0)
    assert srm_p_value(500.0, 3) < 1e-10


def test_assign_period_boundaries():
    started_at = pd.Series(
        pd.to_datetime(
            [
                "2013-06-24 23:59:59",
                "2013-06-25 00:00:00",
                "2014-01-10 23:59:59",
                "2014-01-11 00:00:00",
            ]
        )
    )
    assert list(assign_period(started_at)) == [
        "before window",
        "flagged window",
        "flagged window",
        "after window",
    ]


def test_reliable_test_ids_filters_period_and_srm():
    balance = pd.DataFrame(
        {
            "test_id": ["before_ok", "window_ok", "after_ok", "after_srm"],
            "started_at": pd.to_datetime(
                ["2013-03-01", "2013-09-01", "2014-03-01", "2014-03-01"]
            ),
            "chi_square_stat": [1.0, 1.0, 1.0, 500.0],
            "degrees_of_freedom": [3, 3, 3, 3],
        }
    )
    assert reliable_test_ids(balance, "after window") == {"after_ok"}
    assert reliable_test_ids(balance, "before window") == {"before_ok"}