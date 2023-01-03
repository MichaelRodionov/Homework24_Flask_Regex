from typing import TextIO, Iterator

from classes.file_handler import FileHandler


# ----------------------------------------------------------------
# class UserRequest to handle user request
class UserRequest:
    def __init__(self, params: dict) -> None:
        """
        Constructor for UserRequest
        :param params: dict of parameters (filename, commands, values)
        """
        self.__params = params

    @property
    def params(self) -> dict:
        """
        Getter for params
        :return: dict of params
        """
        return self.__params

    @params.setter
    def params(self, params: dict) -> None:
        """
        Setter for params
        :param params: dict of params
        :return: None
        """
        self.__params = params

    def get_params(self) -> dict:
        """
        Method to get a dictionary of params, formed by keys request_1 and request_2
        :return: dict of requests params
        """
        param_dict = {
            'request_1': (self.params.get('cmd1'), self.params.get('value1')),
            'request_2': (self.params.get('cmd2'), self.params.get('value2'))
        }
        return param_dict

    def get_result(self, file: TextIO) -> Iterator:
        """
        Method to create object for file handler and get final result
        :param file: our data
        :return: result of handle
        """
        self.params: dict = self.get_params()
        file_handler: FileHandler = FileHandler(file, self.params)
        return file_handler.get_result()
