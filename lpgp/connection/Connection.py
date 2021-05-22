# encoding = utf-8
# using namespace std
from .Configurations import Configurations
from pymysql import Connection as MySQLConnection
from pymysql.cursors import Cursor
from typing import AnyStr


class Connection:
    """

    """

    __conf: Configurations = None
    __conn: MySQLConnection = None

    # Exceptions
    class NotConnectedError(BaseException):
        """"""

    class AlreadyConnectedError(BaseException):
        """"""

    @property
    def conn(self) -> MySQLConnection:
        """

        """
        if not self.is_connected: raise self.NotConnectedError("The connector isn't connected")
        return self.__conn

    @property
    def conf(self) -> Configurations:
        """

        """
        if not self.is_connected: raise self.NotConnectedError("The connector isn't connected")
        return self.__conf

    @property
    def is_connected(self) -> bool:
        """

        """
        return self.__conn is None or self.__conn == None

    def __cursor(self) -> Cursor:
        """

        """
        return self.__conn.cursor()

    def __load_conf(self, conf: Configurations):
        """

        """
        if self.is_connected: raise self.AlreadyConnectedError("The connector is already connected")
        self.__conf = conf
        self.__conn  = MySQLConnection(
            host=self.__conf.lpgp_mysql_host,
            user=self.__conf.lpgp_mysql_usr,
            password=self.__conf.lpgp_mysql_passwd,
            database=self.__conf.lpgp_mysql_db
        )

    def __load_path(self, path: AnyStr):
        """

        """
        if self.is_connected: raise self.AlreadyConnectedError("The connector is already connected!")
        self.__conf = Configurations(path)
        self.__conn = MySQLConnection(
            host=self.__conf.lpgp_mysql_host,
            user=self.__conf.lpgp_mysql_usr,
            password=self.__conf.lpgp_mysql_passwd,
            database=self.__conf.lpgp_mysql_db
        )

    def __init__(self, conf):
        """

        """
        if type(conf) is Configurations: self.__load_conf(conf)
        elif type(conf) is AnyStr or type(conf) is str: self.__load_path(conf)
        else: raise RuntimeError("Invalid type of configurations to connect")
