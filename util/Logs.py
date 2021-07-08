# encoding = UTF-8
# using namespace std
from typing import AnyStr
from datetime import datetime
from time import strftime, strptime


class Logger:
    """

    """
    __log_path: AnyStr = None


    def __init__(self, path: AnyStr):
        """

        """
        self.__log_path = path

    @property
    def logs(self) -> str:
        """

        """
        with open(self.__log_path, "r+") as log:
            con = log.read()
        return con

    @property
    def file(self) -> AnyStr:
        """

        """
        return self.__log_path

    def __add__(self, line: str):
        """

        """
        with open(self.__log_path, "w+") as log:
            log.write(self.logs + "\n" + line)
    
