# custom error classes
class BaseError(Exception):
    message = 'Unknown error'


class EmptyArgs(BaseError):
    message = 'Arguments must not be empty'


class WrongArgs(BaseError):
    message = 'Wrong arguments keys'


class SortValue(BaseError):
    message = 'Should be asc or desc value'


class MapValue(BaseError):
    message = 'Map value must be integer'


class LimitValue(BaseError):
    message = 'Limit value must be integer'


