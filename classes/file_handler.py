import re
from typing import TextIO, Any, Iterator, Callable, Iterable

from utils.constants import SORT_PARAMS, COMMANDS
from utils.exceptions import LimitValue, SortValue, MapValue, WrongArgs


# ----------------------------------------------------------------
# class FileHandler to handle file
class FileHandler:
    def __init__(self, file: TextIO, params: dict, result: Any = None) -> None:
        """
        CConstructor for FileHandler
        :param file: file to handle with
        :param params: collection of params (commands, values)
        :param result: result of handle
        """
        self.__file: TextIO = file
        self.__params: dict = params
        self.__result: Any = result

    @property
    def params(self) -> dict:
        """
        Getter for params
        :return: private attribute __params
        """
        return self.__params

    @property
    def file(self) -> TextIO:
        """
        Getter for file
        :return: private attribute __file
        """
        return self.__file

    @property
    def result(self) -> Any:
        """
        Getter for result
        :return: private attribute __result
        """
        return self.__result

    @result.setter
    def result(self, result: Any) -> None:
        """
        Setter for result
        :param result: new data to overwrite private attribute __result
        :return: overwritten attribute __result
        """
        self.__result = result

    def get_result(self) -> Any:
        """
        Method to start execution and get final result
        :return: result of handle
        """
        self.execute()
        return self.result

    def execute(self) -> None:
        """
        Main method of file handle. Runs first command with first value, then - second with second value.
        Finally, used setter to overwrite private attribute __result
        :return: None
        """
        result: map = map(lambda v: v.strip(), self.file)

        command_1, value_1 = self.params['request_1']
        command_2, value_2 = self.params['request_2']

        if command_1 and command_2 not in COMMANDS:
            raise WrongArgs
        else:
            result1: Iterable[str] = self.get_command()[command_1](result, value_1)
            result2: Iterable[str] = self.get_command()[command_2](result1, value_2)
            self.result: Iterator = result2

    def get_command(self) -> dict[str, Callable[..., Iterable[str]]]:
        """
        Method forms dictionary where keys are commands names and values are methods to handle file
        :return: dict with commands
        """
        commands: dict = {
            'filter': self.__filter,
            'map': self.__map,
            'unique': self.__unique,
            'sort': self.__sort,
            'limit': self.__limit,
            'regex': self.__regex
        }
        return commands

    @staticmethod
    def __filter(res: Any, value: str) -> Iterator:
        """
        Method to filter data by given value
        :param res: our data
        :param value: filter value
        :return: filter object
        """
        return filter(lambda text: value in text, res)

    @staticmethod
    def __map(res: Any, value: str) -> Iterator:
        """
        Method to map data by given column
        :param res: our data
        :param value: column number to map
        :return: map object
        """
        try:
            column: int = int(value)
            return map(lambda text: text.split(' ')[column], res)
        except TypeError:
            raise MapValue

    @staticmethod
    def __unique(res: Any, value: str ='') -> Iterator:
        """
        Method to get unique data
        :param res: our data
        :param value: ''
        :return: iterator object of unique data
        """
        return iter(set(res))

    @staticmethod
    def __sort(res: Any, value_order: str) -> Iterator:
        """
        Method to sort data by asc or desc
        :param res: our data
        :param value_order: asc or desc
        :return: sorted object
        """
        if value_order not in SORT_PARAMS:
            raise SortValue
        return iter(sorted(res, reverse=False if value_order == 'asc' else True))

    @staticmethod
    def __limit(res: Any, value_limit: str) -> Iterator:
        """
        Method to limit the output of the final result
        :param res: our data
        :param value_limit: limit of data size
        :return: limited list of data
        """
        try:
            limit = int(value_limit)
            return iter(list(res)[:limit])
        except ValueError:
            raise LimitValue

    @staticmethod
    def __regex(res: Any, value_regexp: str) -> list:
        """
        Method to filter data by regular expression
        :param res: our data
        :param value_regexp: regular expression
        :return: filtered result
        """
        return re.findall(value_regexp, ''.join(res))
