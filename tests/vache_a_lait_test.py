import pytest

from vaches.exceptions import InvalidVacheException
from vaches.vache_a_lait import VacheALait


# -------------------------
# RUMINATION -> PRODUCTION/ STOCKAGE DE LAIT
# -------------------------

def test_should_increase_lait_disponible_given_positive_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == VacheALait.RENDEMENT_LAIT * 10.0


def test_should_increase_lait_total_produit_given_positive_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)

    # Act
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_total_produit == VacheALait.RENDEMENT_LAIT * 10.0


def test_should_return_lait_produced_given_positive_panse_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)

    # Act
    lait = vache.ruminer()

    # Assert (1 assertion métier)
    assert lait == VacheALait.RENDEMENT_LAIT * 10.0


def test_should_accumulate_lait_disponible_given_two_ruminations():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()  # première rumination -> +RENDEMENT_LAIT * 10

    # Act
    # on "re-remplit" la panse pour simuler un nouveau cycle de vie
    vache.brouter(4.0)
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == VacheALait.RENDEMENT_LAIT * (10.0 + 4.0)


# -------------------------
# TRAITE
# -------------------------

def test_should_decrease_lait_disponible_given_valid_litres_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()  # lait_disponible = RENDEMENT_LAIT * 10

    # Act
    vache.traire(3.0)

    # Assert (1 assertion métier)
    assert vache.lait_disponible == (VacheALait.RENDEMENT_LAIT * 10.0) - 3.0


def test_should_return_litres_given_valid_litres_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()

    # Act
    litres_trais = vache.traire(3.0)

    # Assert (1 assertion métier)
    assert litres_trais == 3.0


def test_should_increase_lait_total_traite_given_valid_litres_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()

    # Act
    vache.traire(3.0)

    # Assert (1 assertion métier)
    assert vache.lait_total_traite == 3.0


def test_should_accumulate_lait_total_traite_given_two_traite_operations():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()

    # Act
    vache.traire(2.0)
    vache.traire(3.0)

    # Assert (1 assertion métier)
    assert vache.lait_total_traite == 5.0


@pytest.mark.parametrize("litres", [0.0, -1.0])
def test_should_raise_invalid_vache_exception_given_non_positive_litres_when_traire(litres):
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.traire(litres)


def test_should_raise_invalid_vache_exception_given_litres_greater_than_lait_disponible_when_traire():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)
    vache.ruminer()  # lait_disponible = RENDEMENT_LAIT*10

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.traire(vache.lait_disponible + 0.0001)


# -------------------------
# BROUTEMENT TYPÉ INTERDIT SUR VACHEALait
# -------------------------

def test_should_raise_invalid_vache_exception_given_typed_food_when_brouter_on_vache_a_lait():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=10.0, age=5)

    # Act / Assert
    with pytest.raises(InvalidVacheException):
        vache.brouter(2.0, nourriture="FOIN")


# -------------------------
# Test de la production de lait
# -------------------------

def _produire_lait_jusqua(vache: VacheALait, cible_lait: float) -> None:
    """
    Produit du lait (via brouter + ruminer) jusqu'à atteindre exactement cible_lait.
    Hypothèse TP : RENDEMENT_LAIT constant, production linéaire.
    """
    if cible_lait < 0:
        raise ValueError("cible_lait doit être >= 0")
    if cible_lait > VacheALait.PRODUCTION_LAIT_MAX:
        raise ValueError("cible_lait ne doit pas dépasser PRODUCTION_LAIT_MAX")

    # On boucle en produisant par cycles (évite de dépasser PANSE_MAX)
    while vache.lait_disponible < cible_lait:
        restant = cible_lait - vache.lait_disponible
        panse_necessaire = restant / VacheALait.RENDEMENT_LAIT

        # sécurisation: ne pas dépasser la panse max
        quantite = min(panse_necessaire, vache.PANSE_MAX)

        vache.brouter(quantite)
        vache.ruminer()

        # Si on a dépassé à cause d'arrondis, on stoppe et on laisse le test échouer
        if vache.lait_disponible > cible_lait + 1e-9:
            break


def test_should_allow_ruminer_given_lait_production_reaches_production_max_exactly():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=0.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX - 1.0)  # on se met à 39 L

    # Act
    panse = 1.0 / VacheALait.RENDEMENT_LAIT  # produit exactement 1 L
    vache.brouter(panse)
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == pytest.approx(VacheALait.PRODUCTION_LAIT_MAX)


def test_should_raise_invalid_vache_exception_given_lait_production_exceeds_production_max_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=0.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX - 0.5)  # 39.5 L

    # Act / Assert
    # On tente de produire 1 L -> dépasserait 40 L
    panse = 1.0 / VacheALait.RENDEMENT_LAIT
    vache.brouter(panse)

    with pytest.raises(InvalidVacheException):
        vache.ruminer()


def test_should_allow_ruminer_again_given_traite_frees_capacity_below_production_max():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=0.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX)  # lait_disponible = 40 L
    vache.traire(10.0)  # lait_disponible = 30 L (capacité libérée: 10 L)

    # Act
    # On produit exactement 10 L (pour remonter à 40 L)
    panse = 10.0 / VacheALait.RENDEMENT_LAIT
    vache.brouter(panse)
    vache.ruminer()

    # Assert (1 assertion métier)
    assert vache.lait_disponible == pytest.approx(VacheALait.PRODUCTION_LAIT_MAX)


def test_should_raise_invalid_vache_exception_given_production_max_reached_when_ruminer():
    # Arrange
    vache = VacheALait(petitNom="Lola", poids=500.0, panse=0.0, age=5)
    _produire_lait_jusqua(vache, VacheALait.PRODUCTION_LAIT_MAX)  # lait_disponible = 40 L

    # Act / Assert
    # Ruminer est possible (panse > 0) mais le stockage ferait dépasser le max
    vache.brouter(0.1)

    with pytest.raises(InvalidVacheException):
        vache.ruminer()