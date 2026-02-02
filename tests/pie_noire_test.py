import pytest

from vaches.exceptions import InvalidVacheException
from vaches.nourriture.TypeNourriture import TypeNourriture
from vaches.pie_noire import PieNoire
from vaches.vache_a_lait import VacheALait


# -------------------------
# TACHES (invariants)
# -------------------------

def test_should_create_pie_noire_given_positive_taches():
    # Arrange / Act
    pie = PieNoire(
        petitNom="Bella",
        poids=520.0,
        panse=10.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )

    # Assert (1 assertion métier)
    assert pie.nb_taches_noires == 18


@pytest.mark.parametrize("nb_taches_blanches", [0, -1])
def test_should_raise_invalid_vache_exception_given_non_positive_white_spots(nb_taches_blanches):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire(
            petitNom="Bella",
            poids=520.0,
            panse=10.0,
            age=6,
            nb_taches_blanches=nb_taches_blanches,
            nb_taches_noires=10,
        )


@pytest.mark.parametrize("nb_taches_noires", [0, -1])
def test_should_raise_invalid_vache_exception_given_non_positive_black_spots(nb_taches_noires):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire(
            petitNom="Bella",
            poids=520.0,
            panse=10.0,
            age=6,
            nb_taches_blanches=10,
            nb_taches_noires=nb_taches_noires,
        )


@pytest.mark.parametrize("nb_taches_blanches", ["12", 12.0, None])
def test_should_raise_invalid_vache_exception_given_non_int_white_spots(nb_taches_blanches):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire(
            petitNom="Bella",
            poids=520.0,
            panse=10.0,
            age=6,
            nb_taches_blanches=nb_taches_blanches,  # type invalide
            nb_taches_noires=10,
        )


@pytest.mark.parametrize("nb_taches_noires", ["18", 18.0, None])
def test_should_raise_invalid_vache_exception_given_non_int_black_spots(nb_taches_noires):
    # Arrange / Act / Assert
    with pytest.raises(InvalidVacheException):
        PieNoire(
            petitNom="Bella",
            poids=520.0,
            panse=10.0,
            age=6,
            nb_taches_blanches=10,
            nb_taches_noires=nb_taches_noires,  # type invalide
        )


# -------------------------
# BROUTER (ration typée)
# -------------------------

def test_should_update_ration_given_typed_brouter():
    # Arrange
    pie = PieNoire(
        petitNom="Bella",
        poids=520.0,
        panse=0.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )

    # Act
    pie.brouter(3.0, TypeNourriture.HERBE)

    # Assert (1 assertion métier)
    assert pie.ration[TypeNourriture.HERBE] == 3.0


def test_should_accumulate_same_food_in_ration_given_two_typed_brouter_calls():
    # Arrange
    pie = PieNoire(
        petitNom="Bella",
        poids=520.0,
        panse=0.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )

    # Act
    pie.brouter(2.0, TypeNourriture.FOIN)
    pie.brouter(1.5, TypeNourriture.FOIN)

    # Assert (1 assertion métier)
    assert pie.ration[TypeNourriture.FOIN] == 3.5


def test_should_not_change_ration_given_primary_brouter_without_type():
    # Arrange
    pie = PieNoire(
        petitNom="Bella",
        poids=520.0,
        panse=0.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )

    # Act
    pie.brouter(2.0)

    # Assert (1 assertion métier)
    assert pie.ration == {}


# -------------------------
# RUMINATION (lait spécialisé + reset ration)
# -------------------------

def test_should_produce_specialized_lait_given_non_empty_ration_when_ruminer():
    # Arrange
    pie = PieNoire(
        petitNom="Bella",
        poids=520.0,
        panse=0.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )
    pie.brouter(2.0, TypeNourriture.HERBE)
    pie.brouter(1.0, TypeNourriture.CEREALES)

    # Act
    lait = pie.ruminer()

    # Assert (1 assertion métier)
    assert lait == (
            VacheALait.RENDEMENT_LAIT
            * (
                    2.0 * PieNoire.COEFFICIENT_LAIT_PAR_NOURRITURE[TypeNourriture.HERBE]
                    + 1.0 * PieNoire.COEFFICIENT_LAIT_PAR_NOURRITURE[TypeNourriture.CEREALES]
            )
    )


def test_should_clear_ration_given_ruminer_was_called():
    # Arrange
    pie = PieNoire(
        petitNom="Bella",
        poids=520.0,
        panse=0.0,
        age=6,
        nb_taches_blanches=12,
        nb_taches_noires=18,
    )
    pie.brouter(2.0, TypeNourriture.HERBE)

    # Act
    pie.ruminer()

    # Assert (1 assertion métier)
    assert pie.ration == {}