# test_point_plan.py
import pytest

from point_plan.point_3d import Point3D

def test_should_init_azimut_to_none_when_no_args_given():
    # Arrange
    point = Point3D()

    # Act
    result = point.azimut

    # Assert (1 assertion métier)
    assert result is None


def test_should_init_azimut_when_args_given():
    # Arrange
    azimut_expected = 30

    # Act
    point = Point3D(1, 2, azimut_expected)

    # Assert (1 assertion métier)
    assert point.azimut == azimut_expected


def test_should_init_abscisse_when_args_given():
    # Arrange
    abscisse_expected = 10

    # Act
    point = Point3D(abscisse_expected, 20, 30)

    # Assert (1 assertion métier)
    assert point.abscisse == abscisse_expected


def test_should_init_ordonnee_when_args_given():
    # Arrange
    ordonnee_expected = 20

    # Act
    point = Point3D(10, ordonnee_expected, 30)

    # Assert (1 assertion métier)
    assert point.ordonnee == ordonnee_expected


def test_should_update_azimut_when_setter_called():
    # Arrange
    point = Point3D(1, 2, 3)
    new_azimut = 99

    # Act
    point.azimut = new_azimut

    # Assert (1 assertion métier)
    assert point.azimut == new_azimut


def test_should_copy_abscisse_when_from_point_called():
    # Arrange
    original = Point3D(5, 8, 12)

    # Act
    copy = Point3D.from_point(original)

    # Assert (1 assertion métier)
    assert copy.abscisse == original.abscisse


def test_should_copy_ordonnee_when_from_point_called():
    # Arrange
    original = Point3D(5, 8, 12)

    # Act
    copy = Point3D.from_point(original)

    # Assert (1 assertion métier)
    assert copy.ordonnee == original.ordonnee


def test_should_copy_azimut_when_from_point_called():
    # Arrange
    original = Point3D(5, 8, 12)

    # Act
    copy = Point3D.from_point(original)

    # Assert (1 assertion métier)
    assert copy.azimut == original.azimut


def test_should_create_distinct_instance_when_from_point_called():
    # Arrange
    original = Point3D(5, 8, 12)

    # Act
    copy = Point3D.from_point(original)

    # Assert (1 assertion métier)
    assert copy is not original


def test_should_format_string_when_str_called():
    # Arrange
    point = Point3D(3, 4, 7)

    # Act
    result = str(point)

    # Assert (1 assertion métier)
    assert result == "Point3D :\nabscisse = 3, ordonnee=4azimut=7"