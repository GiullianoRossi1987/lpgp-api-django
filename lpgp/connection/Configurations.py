# encoding = UTF-8
# using namespace std
from json import loads, dumps
from typing import AnyStr
from base64 import b64encode, b64decode
from binascii import Error as B64Error


class Configurations:
    """
    """

    __conf_file: AnyStr
    __config: dict = dict()

    # Exceptions

    class ConfigurationsAcessError(Exception):
        """

        """


    # Properties

    @property
    def confFile(self) -> AnyStr: return self.__conf_file

    @property
    def raw(self):
        if len(self.__config) == 0: return None
        else: return self.__config["config"]

    @property
    def lpgp_mysql_host(self):
        if len(self.__config) == 0: return None
        else: return self.raw["lpgp"]["mysql_host"]

    @property
    def lpgp_mysql_usr(self):
        if len(self.__config) == 0: return None
        else: return self.raw["lpgp"]["mysql_usr"]

    @property
    def lpgp_mysql_db(self):
        if len(self.__config) == 0: return None
        else: return self.raw["lpgp"]["mysql_db"]

    @property
    def lpgp_mysql_passwd(self):
        if len(self.__config) == 0: return None
        else: return self.raw["lpgp"]["mysql_passwd"]

    @property
    def sv_host(self):
        if len(self.__config) == 0: return None
        else: return self.raw["server"]["hostname"]

    @property
    def sv_port(self):
        if len(self.__config) == 0: return None
        else: return self.raw["server"]["port"]

    @property
    def sv_ctrl_path(self):
        if len(self.__config) == 0: return None
        else: return self.raw["controllers"]["control_path"]

    # Properties setters

    @lpgp_mysql_host.setter
    def lpgp_mysql_host(self, host: str):
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        self.raw["lpgp"]["mysql_host"] = host
        # Commits the changes
        self.__commit()

    @lpgp_mysql_usr.setter
    def lpgp_mysql_usr(self, usr: str):
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        self.raw["lpgp"]["mysql_usr"] = usr
        # Commits the changes
        self.__commit()

    @lpgp_mysql_db.setter
    def lpgp_mysql_db(self, db: str):
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        self.raw["lpgp"]["mysql_db"] = db
        # Commits the changes
        self.__commit()

    @lpgp_mysql_passwd.setter
    def lpgp_mysql_passwd(self, passwd: str):
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        # e_passwd = ""
        if len(passwd) > 0:
            try:
                _ = b64decode(passwd)
                e_passwd = passwd
            except B64Error:
                e_passwd = b64encode(passwd)
        else: e_passwd = ""
        self.raw["lpgp"]["mysql_passwd"] = e_passwd
        # Commits the changes
        self.__commit()

    @sv_host.setter
    def sv_host(self, host: str):
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        self.raw["server"]["hostname"] = host if len(host) > 0 else "0.0.0.0"
        self.__commit()

    @sv_ctrl_path.setter
    def sv_ctrl_path(self, path: str):
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        self.raw["controllers"]["control_path"] = path
        self.__commit()
    # Methods

    def __init__(self, conf):
        """
        """
        if conf is dict:
            self.__config = conf
            self.__conf_file = "internal"
        else:
            with open(conf, "r") as cfl:
                self.__conf_file = conf
                self.__config = loads(cfl.read())

    def __str__(self):
        return dumps(self.__config)

    def __commit(self):
        """

        """
        if len(self.__config) == 0:
            raise self.ConfigurationsAcessError("Can't access the configurations file, there's no one loaded")
        with open(self.__conf_file, "w+") as cfl:
            cfl.write(dumps(self.__config))
