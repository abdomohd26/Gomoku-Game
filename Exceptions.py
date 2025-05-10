class InvalidMove(Exception):
    """Exception raised for invalid moves."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
