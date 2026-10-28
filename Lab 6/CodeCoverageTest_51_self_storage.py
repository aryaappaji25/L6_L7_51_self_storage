
import pytest
from self_storage import rent_due, access_allowed, payment_status


# Code coverage tests: rent_due()

def test_rent_small():
    assert rent_due("small", 1, False, False) == 0


def test_rent_medium():
    assert rent_due("medium", 5, False, False) == 240


def test_rent_large():
    assert rent_due("large", 5, False, False) == 160


def test_rent_member_discount():
    assert rent_due("small", 5, False, True) == 240


def test_rent_large_member():
    assert rent_due("large", 5, False, True) == 160


def test_rent_climate_control():
    assert rent_due("medium", 5, True, False) == 360


def test_rent_extra_over_six():
    assert rent_due("small", 8, False, False) == 490


def test_rent_extra_climate_over_six():
    assert rent_due("small", 8, True, False) == 735


def test_rent_extra_climate_under_six():
    assert rent_due("small", 3, True, False) == 240


def test_rent_unknown_unit():
    with pytest.raises(ValueError):
        rent_due("unknown", 1, False, False)


def test_rent_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


# Code coverage tests: access_allowed()

def test_access_owner_allowed():
    assert access_allowed(12, 4, True) is True


def test_access_owner_denied():
    assert access_allowed(12, 5, True) is False


def test_access_allowed():
    assert access_allowed(12, 2, False) is True


def test_access_too_many_visitors():
    assert access_allowed(12, 5, False) is False


def test_access_before_hours():
    assert access_allowed(5, 1, False) is False


def test_access_after_hours():
    assert access_allowed(23, 1, False) is False


# Code coverage tests: payment_status()

def test_payment_autopay_current():
    assert payment_status(0, True, False) == "current"


def test_payment_manual_current():
    assert payment_status(5, False, False) == "current"


def test_payment_grace():
    assert payment_status(4, False, False) == "grace"


def test_payment_lien():
    assert payment_status(-11, False, False) == "lien"


def test_payment_prior_late_grace():
    assert payment_status(10, False, True) == "grace"


def test_payment_prior_late_current():
    assert payment_status(15, False, True) == "current"


def test_payment_autopay_prior_late():
    assert payment_status(10, True, True) == "current"


def test_payment_autopay_lien():
    assert payment_status(-16, True, False) == "lien"
