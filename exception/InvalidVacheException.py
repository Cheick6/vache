class InvalidVacheException(Exception):
    """
    Exception levée quand une opération sur une Vache est invalide.
    """
    def __init__(self, message="Opération fausse sur la vache"):
        self.message = message
        super().__init__(self.message)