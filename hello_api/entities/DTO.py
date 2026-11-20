class ResultDTO:
    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message
    @classmethod
    def resultadoUser(cls, user: object):
        return cls(success=False, message="")


