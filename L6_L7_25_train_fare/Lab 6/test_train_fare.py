import pytest
from train_fare import base_fare, concession, tatkal_charge


# BASE FARE TESTS
def test_sleeper_fare():
    assert base_fare("SL", 500) == 500


def test_all_travel_classes():
    assert base_fare("3A", 100) == 200
    assert base_fare("2A", 100) == 300
    assert base_fare("1A", 100) == 500


def test_minimum_fare():
    assert base_fare("SL", 10) == 50


def test_unknown_travel_class():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("AC", 100)


def test_zero_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


def test_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", -10)


# CONCESSION TESTS
def test_adult_no_concession():
    assert concession(30, "M", False) == 0


def test_child_below_five():
    assert concession(4, "M", False) == 100


def test_child_age_five():
    assert concession(5, "M", False) == 50


def test_child_age_twelve():
    assert concession(12, "M", False) == 50


def test_teenager_no_concession():
    assert concession(13, "M", False) == 0


def test_senior_citizen_female():
    assert concession(60, "F", False) == 50


def test_senior_citizen_male():
    assert concession(60, "M", False) == 40


def test_senior_citizen_other_gender():
    assert concession(65, "X", False) == 40


def test_tatkal_no_concession():
    assert concession(4, "F", True) == 0
    assert concession(30, "M", True) == 0
    assert concession(70, "F", True) == 0


# TATKAL CHARGE TESTS
def test_sleeper_tatkal_charge():
    assert tatkal_charge("SL", 1500) == 150


def test_other_class_tatkal_charge():
    assert tatkal_charge("3A", 500) == 150


def test_tatkal_minimum_charge():
    assert tatkal_charge("SL", 500) == 100
    assert tatkal_charge("3A", 100) == 100


def test_tatkal_maximum_charge():
    assert tatkal_charge("SL", 5000) == 400
    assert tatkal_charge("2A", 2000) == 400
