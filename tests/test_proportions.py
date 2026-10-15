import pytest

from src.stats.proportions import (
    minimum_detectable_effect,
    sample_size_per_arm,
    two_proportion_test,
)

Q2_POOLED_CTR = 712 / 30164


def test_identical_arms_have_no_difference():
    result = two_proportion_test(50, 1000, 50, 1000)
    assert result.diff == 0
    assert result.p_value == pytest.approx(1.0)
    assert result.ci_low < 0 < result.ci_high


def test_large_difference_is_significant():
    result = two_proportion_test(100, 10000, 200, 10000)
    assert result.p_value < 0.001
    assert result.ci_low > 0
    assert result.relative_lift == pytest.approx(1.0)


def test_swapping_arms_flips_the_sign():
    ab = two_proportion_test(362, 15194, 350, 14970)
    ba = two_proportion_test(350, 14970, 362, 15194)
    assert ab.diff == pytest.approx(-ba.diff)
    assert ab.p_value == pytest.approx(ba.p_value)


def test_rejects_zero_impressions():
    with pytest.raises(ValueError):
        two_proportion_test(0, 0, 10, 100)


def test_q2_minimum_detectable_effect():
    mde = minimum_detectable_effect(Q2_POOLED_CTR, 15194, 14970)
    assert mde == pytest.approx(0.0049, rel=0.01)


def test_q2_sample_size_for_ten_percent_lift():
    assert sample_size_per_arm(Q2_POOLED_CTR, 0.10) == pytest.approx(64934, rel=0.001)