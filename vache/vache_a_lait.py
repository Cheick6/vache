from vache.vache import Vache
from exception.InvalidVacheException import InvalidVacheException

class VacheALait(Vache):
    """
    Une vache spécialisée dans la production de lait.
    Elle transforme le contenu de sa panse en lait plutôt qu'en poids.
    """

    RENDEMENT_LAIT = 1.1 
    PRODUCTION_LAIT_MAX = 50.0 

    def __init__(self, petitNom: str, poids: float, age: int):
        super().__init__(petit_nom=petitNom, poids=poids, age=age)
        
        self._lait_disponible = 0.0
        self._lait_total_produit = 0.0
        self._lait_total_traite = 0.0


    @property
    def lait_disponible(self):
        return self._lait_disponible

    @property
    def lait_total_produit(self):
        return self._lait_total_produit

    @property
    def lait_total_traite(self):
        return self._lait_total_traite


    def ruminer(self):
        """
        Surcharge de la méthode ruminer.
        Transforme l'herbe (panse) en lait disponible.
        """
        if self._panse <= 0:
            raise InvalidVacheException("Impossible de ruminer le ventre vide.")

        production_potentielle = self._panse * self.RENDEMENT_LAIT

        
        if self._lait_disponible + production_potentielle > self.PRODUCTION_LAIT_MAX:
             raise InvalidVacheException(f"Production excessive ! Le pis déborde. Max : {self.PRODUCTION_LAIT_MAX}")

        self._lait_disponible += production_potentielle
        self._lait_total_produit += production_potentielle
        
        self._panse = 0.0

    def traire(self, litres: float) -> float:
        """
        Récupère une quantité de lait disponible.
        """
        if litres <= 0:
            raise InvalidVacheException("On ne peut pas traire une quantité négative ou nulle.")
        
        
        if litres > self._lait_disponible:
            raise InvalidVacheException(f"Pas assez de lait. Demandé: {litres}, Dispo: {self._lait_disponible}")

        self._lait_disponible -= litres
        self._lait_total_traite += litres
        
        return litres

    def __str__(self):
        parent_str = super().__str__()
        return f"{parent_str}, Lait disponible : {self._lait_disponible} L, Lait total trait : {self._lait_total_traite} L"