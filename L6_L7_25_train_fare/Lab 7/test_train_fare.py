"""Property-based tests for the train fare input-processing functions."""

import pytest
from hypothesis import given, strategies as st

from train_fare import BERTHS, berth_type, journey_distance, parse_pnr


@given(st.text() | st.none() | st.integers() | st.lists(st.integers()))
def test_parse_pnr_handles_fuzzed_inputs(value):
    """Accept a ten digit PNR, and reject malformed or non-string values."""
    if isinstance(value, str) and len(value) == 10 and value.isascii() and value.isdigit():
        assert parse_pnr(value) == (int(value[0]), int(value[1:]))
    else:
        with pytest.raises(ValueError):
            parse_pnr(value)


@given(st.text(alphabet="0123456789", min_size=10, max_size=10))
def test_parse_pnr_valid_values(pnr):
    assert parse_pnr(pnr) == (int(pnr[0]), int(pnr[1:]))


@given(st.text() | st.none() | st.integers() | st.lists(st.integers()))
def test_journey_distance_handles_fuzzed_inputs(value):
    """For arbitrary inputs, only a well-formed CSV or ValueError is allowed."""
    if isinstance(value, str):
        parts = value.split(",")
        try:
            numbers = [int(part.strip()) for part in parts]
        except ValueError:
            with pytest.raises(ValueError):
                journey_distance(value)
        else:
            assert journey_distance(value) == numbers[-1] - numbers[0]
    else:
        with pytest.raises(ValueError):
            journey_distance(value)


@given(st.lists(st.integers(), min_size=1, max_size=20))
def test_journey_distance_valid_values(distances):
    csv = ",".join(map(str, distances))
    assert journey_distance(csv) == distances[-1] - distances[0]


@given(st.text() | st.none() | st.integers() | st.lists(st.integers()))
def test_berth_type_handles_fuzzed_inputs(value):
    """Accept a coach-positive-seat pair; reject malformed and non-string data."""
    if isinstance(value, str):
        pieces = value.split("-")
        seat_number = pieces[1].strip() if len(pieces) == 2 else ""
        if len(pieces) == 2 and pieces[0].strip() and seat_number.isascii() and seat_number.isdigit():
            number = int(seat_number)
            if number > 0:
                assert berth_type(value) == (pieces[0].strip().upper(), BERTHS[number % 8])
                return
    with pytest.raises(ValueError):
        berth_type(value)


@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", min_size=1, max_size=5),
    st.integers(min_value=1, max_value=100000),
)
def test_berth_type_valid_values(coach, number):
    assert berth_type(f"{coach.lower()}-{number}") == (coach, BERTHS[number % 8])
