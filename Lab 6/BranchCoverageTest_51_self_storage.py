
import pytest
from self_storage import rent_due, access_allowed, payment_status


# Branch coverage tests: rent_due()

def test_unknown_unit_branch():
    with pytest.raises(ValueError):
        rent_due("extra_large", 2, False, False)


def test_negative_months_branch():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


def test_member_small_unit_branch():
    assert rent_due("small", 5, False, True) == 240


def test_member_medium_unit_branch():
    assert rent_due("medium", 5, False, True) == 160


def test_non_member_branch():
    assert rent_due("medium", 5, False, False) == 240


def test_large_unit_member_condition():
    assert rent_due("large", 5, False, True) == 160


def test_no_extra_branch():
    assert rent_due("small", 1, False, False) == 0


def test_exact_covered_months_branch():
    assert rent_due("medium", 2, False, False) == 0


def test_climate_rate_branch():
    assert rent_due("medium", 5, True, False) == 360


def test_non_climate_rate_branch():
    assert rent_due("medium", 5, False, False) == 240


def test_extra_not_over_six_branch():
    assert rent_due("small", 7, False, False) == 480


def test_extra_over_six_branch():
    assert rent_due("small", 8, False, False) == 490


def test_extra_over_six_climate_branch():
    assert rent_due("small", 8, True, False) == 735


def test_extra_over_six_without_climate_branch():
    assert rent_due("small", 8, False, False) == 490


# Branch coverage tests: access_allowed()

def test_owner_within_limit():
    assert access_allowed(12, 4, True) is True


def test_owner_over_limit():
    assert access_allowed(12, 5, True) is False


def test_owner_access_ignores_hour():
    assert access_allowed(23, 2, True) is True


def test_non_owner_within_limit():
    assert access_allowed(12, 2, False) is True


def test_non_owner_over_limit():
    assert access_allowed(12, 3, False) is False


def test_before_opening_hour():
    assert access_allowed(5, 1, False) is False


def test_opening_hour_boundary():
    assert access_allowed(6, 1, False) is True


def test_closing_hour_boundary():
    assert access_allowed(22, 1, False) is True


def test_after_closing_hour():
    assert access_allowed(23, 1, False) is False


# Branch coverage tests: payment_status()

def test_autopay_cutoff():
    assert payment_status(0, True, False) == "current"


def test_manual_payment_cutoff():
    assert payment_status(5, False, False) == "current"


def test_prior_late_increases_cutoff():
    assert payment_status(10, False, True) == "grace"


def test_current_with_prior_late():
    assert payment_status(15, False, True) == "current"


def test_grace_period():
    assert payment_status(4, False, False) == "grace"


def test_lien_status():
    assert payment_status(-11, False, False) == "lien"


def test_autopay_with_prior_late():
    assert payment_status(10, True, True) == "current"


def test_autopay_grace_status():
    assert payment_status(-1, True, False) == "grace"


def test_autopay_lien_status():
    assert payment_status(-16, True, False) == "lien"
