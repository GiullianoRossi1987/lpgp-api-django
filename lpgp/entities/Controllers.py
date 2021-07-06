# encoding = UTF-8
# using namespace std
from ..connection.Configurations import Configurations
from typing import AnyStr
from json import loads, dumps
from datetime import datetime
from time import strftime, strptime



class Controller:
    """

    """
    _path: AnyStr = None
    _buf: dict = None
    _rbuf: str = None

    # Exceptions

    class InvalidToken(BaseException):
        """

        """

        def __init__(self, tk: str):
            """

            """
            super("Invalid token: " + tk)


    def __init__(self, src):
        """

        """
        if type(src) is Configurations:
            self._path = src.sv_ctrl_path
        elif type(src) is str or type(src) is AnyStr:
            self._path = src
        else: raise TypeError("Invalid type of controllers file source")
        # Works on the received file
        with open(self._path, "r+") as ctrl:
            self._rbuf = ctrl.read()
            self._buf = loads(self._rbuf)

    @property
    def path(self): return self._path

    @property
    def data(self): return self._buf

    @property
    def raw_json(self): return self._rbuf

    @property
    def sdownloads(self): return self._buf["sdownloads"]

    @property
    def suploads(self): return self._buf["suploads"]

    @property
    def cdownloads(self): return self._buf["cdownloads"]

    @property
    def cuploads(self): return self._buf["cuploads"]

    def _commit(self):
        """

        """
        with open(self._path, "w") as ctrl:
            self._rbuf = dumps(self._buf)
            ctrl.write(self._rbuf)

    def get_sd(self, tk: str) -> tuple:
        """

        """
        return tuple(x for x in filter(lambda s: s["dtk"] == tk, self.sdownloads))

    def get_su(self, tk: str) -> tuple:
        """

        """
        return tuple(x for x in filter(lambda s: s["dtk"] == tk, self.suploads))

    def get_cd(self, tk: str) -> tuple:
        """

        """
        return tuple(x for x in filter(lambda s: s["dtk"] == tk, self.cdownloads))

    def get_cu(self, tk: str) -> tuple:
        """

        """
        return tuple(x for x in filter(lambda s: s["dtk"] == tk, self.cuploads))
