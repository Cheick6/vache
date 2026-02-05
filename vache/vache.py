from exception.InvalidVacheException import InvalidVacheException
from exception.InvalidVacheException import InvalidVacheException

class Vache:
    """
    Classe représentant une vache avec validation stricte de l'état pour passer les tests.
    """
    
    AGE_MAX = 25
    POIDS_MAX = 1000.0
    PANSE_MAX = 50.0
    MIN_PANSE = 2.0
    RENDEMENT_RUMINATION = 0.25
    NEXT_ID = 1
    
    def __init__(self, petit_nom: str, poids: float, age: int):
        if not petit_nom or not petit_nom.strip():
            raise InvalidVacheException("Le petit nom ne peut pas être vide.")
        
        if poids < 0:
            raise InvalidVacheException("Le poids ne peut pas être négatif.")
            
        if age < 0 or age > self.AGE_MAX:
            raise InvalidVacheException(f"L'âge doit être compris entre 0 et {self.AGE_MAX}.")

        self._id = Vache.NEXT_ID
        Vache.NEXT_ID += 1
        
        self._petit_nom = petit_nom
        self._poids = poids
        self._age = age
        self._panse = 0.0

    @property
    def id(self):
        return self._id

    @property
    def petit_nom(self): 
        return self._petit_nom
    
    @property
    def poids(self):
        return self._poids

    @property
    def panse(self):
        return self._panse
    
    @property
    def age(self):
        return self._age


    def brouter(self, quantite: float, nourriture=None):
        """
        La vache mange. Elle ne supporte pas le paramètre 'nourriture' (spécifique aux tests).
        """
        if nourriture is not None:
            raise InvalidVacheException("Cette vache ne gère pas les types de nourriture.")

        if quantite <= 0:
            raise InvalidVacheException("La quantité broutée doit être positive.")

        
        if self._panse + quantite > self.PANSE_MAX:
            raise InvalidVacheException(f"La panse est pleine ! Max : {self.PANSE_MAX}")

        self._panse += quantite

    def ruminer(self):
        """
        Transforme le contenu de la panse en poids selon le rendement.
        """
        if self._panse <= 0:
            raise InvalidVacheException("Rien à ruminer dans la panse.")

        gain_poids = self._panse * self.RENDEMENT_RUMINATION
        self._poids += gain_poids
        
        self._panse = 0.0

    def vieillir(self):
        """
        Augmenter âge vache de 1 an.
        """
        if self._age >= self.AGE_MAX:
            raise InvalidVacheException("La vache a atteint son âge limite.")
            
        self._age += 1

    def __str__(self):
        return f"id = {self._id}, petitNom ={self._petit_nom}, poids = {self._poids}, panse ={self._panse}, age ={self._age}"