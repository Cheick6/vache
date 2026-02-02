# test_point_plan.py
import pytest

from point_plan.point_plan import PointPlan


def test_should_init_abscisse_to_none_when_no_args_given():
        # Arrange
        point = PointPlan()

        # Act
        result = point.abscisse

        # Assert (1 assertion métier)
        assert result is None


def test_should_init_ordonnee_to_none_when_no_args_given():
    # Arrangepytest
    point = PointPlan()

    # Act
    result = point.ordonnee

    # Assert (1 assertion métier)
    assert result is None


def test_should_init_abscisse_when_args_given():
    # Arrange
    abscisse_expected = 10

    # Act
    point = PointPlan(abscisse_expected, 20)

    # Assert (1 assertion métier)
    assert point.abscisse == abscisse_expected


def test_should_init_ordonnee_when_args_given():
    # Arrange
    ordonnee_expected = 20

    # Act
    point = PointPlan(10, ordonnee_expected)

    # Assert (1 assertion métier)
    assert point.ordonnee == ordonnee_expected


def test_should_return_abscisse_when_getter_called():
    # Arrange
    point = PointPlan(7, 9)

    # Act
    result = point.abscisse

    # Assert (1 assertion métier)
    assert result == 7


def test_should_return_ordonnee_when_getter_called():
    # Arrange
    point = PointPlan(7, 9)

    # Act
    result = point.ordonnee

    # Assert (1 assertion métier)
    assert result == 9


def test_should_update_abscisse_when_setter_called():
    # Arrange
    point = PointPlan(1, 2)
    new_abscisse = 42

    # Act
    point.abscisse = new_abscisse

    # Assert (1 assertion métier)
    assert point.abscisse == new_abscisse


def test_should_update_ordonnee_when_setter_called():
    # Arrange
    point = PointPlan(1, 2)
    new_ordonnee = 99

    # Act
    point.ordonnee = new_ordonnee

    # Assert (1 assertion métier)
    assert point.ordonnee == new_ordonnee


def test_should_accept_string_abscisse_when_setter_called_given_no_validation():
    # Arrange
    point = PointPlan(1, 2)
    new_abscisse = "X"

    # Act
    point.abscisse = new_abscisse

    # Assert (1 assertion métier)
    assert point.abscisse == "X"


def test_should_accept_string_ordonnee_when_setter_called_given_no_validation():
    # Arrange
    point = PointPlan(1, 2)
    new_ordonnee = "Y"

    # Act
    point.ordonnee = new_ordonnee

    # Assert (1 assertion métier)
    assert point.ordonnee == "Y"


def test_should_format_string_when_str_called():
    # Arrange
    point = PointPlan(3, 4)

    # Act
    result = str(point)

    # Assert (1 assertion métier)
    assert result == "\nabscisse = 3, ordonnee=4"


def test_should_format_string_with_none_when_str_called_and_values_are_none():
    # Arrange
    point = PointPlan()

    # Act
    result = str(point)

    # Assert (1 assertion métier)
    assert result == "\nabscisse = None, ordonnee=None"

def test_should_create_new_point_with_same_coordinates_when_from_point_called():
    # Arrange
    original = PointPlan(5, 8)

    # Act
    copy = PointPlan.from_point(original)

    # Assert (1 assertion métier)
    assert copy.abscisse == original.abscisse

def test_should_create_distinct_instance_when_from_point_called():
    # Arrange
    original = PointPlan(5, 8)

    # Act
    copy = PointPlan.from_point(original)

    # Assert (1 assertion métier)
    assert copy is not original