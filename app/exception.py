class BaseException(Exception):
    status_code = 500
    
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)
        
        
class BadRequestError(BaseException):
    status_code= 400
    
class UnauthorizedError(BaseException):
    status_code = 401

class NotFoundError(BaseException):
    status_code = 404
    
class ConflictError(BaseException):
    status_code = 409