# encoding = utf-8
# using namespace std
from ..connection.Connection import Connection
from ..connection.Configurations import Configurations
from typing import Tuple, AnyStr
from datetime import datetime
from json import loads as json_loads
from json import dumps as json_dumps
from time import strftime, strptime
from .Proprietaries import Proprietary, ProprietariesTable


class Client:
    """

    """

    id: int = None
    name: str = None
    token: str = None
    prop: Proprietary = None
    is_root: bool = True

    def __init__(self, lake = None):
        """

        """
        if type(lake) is list or type(lake) is tuple:
            self.id = int(lake[0])
            self.name = str(lake[1])
            self.token = str(lake[2])
            if type(lake[3]) is Proprietary:
                self.prop = lake[3]
            else:
                _s = Proprietary()
                _s.cd = int(lake[3])
                _st = ProprietariesTable(Configurations("config.json"))
                self.prop = _st.qr_proprietary(_s)[0]
                del _st
                del _s
            self.is_root = bool(int(lake[4]))
        elif type(lake) is dict:
            self.id = int(lake["cd_client"])
            self.name = str(lake["nm_client"])
            self.token = str(lake["tk_client"])
            if type(lake["id_proprietary"]) is Proprietary:
                self.prop = lake["id_proprietary"]
            else:
                _s = Proprietary()
                _s.cd = int(lake["id_proprietary"])
                _st = ProprietariesTable(Configurations("config.json"))
                self.prop = _st.qr_proprietary(_s)[0]
                del _st
                del _s
            self.is_root = bool(int(lake["vl_root"]))
        elif type(lake) is None or lake == None: pass
        else:
            raise TypeError("Invalid value for client data importation")

    def __tuple__(self) -> tuple:
        """

        """
        return self.id, self.name, self.token, self.prop, self.is_root

    def __str__(self):
        """

        """
        return ", ".join(map(lambda i: str(i) if type(i) is not Proprietary else str(i.cd),
         self.__tuple__()))

    def __dict__(self):
        """

        """
        return {
            "cd_client": self.id,
            "nm_client": self.name,
            "tk_client": self.token,
            "id_proprietary": self.prop.cd,
            "vl_root": self.is_root
        }

    def enc_d(self) -> dict:
        """

        """
        return {
            "Client": self.id,
            "Token": self.token,
            "Proprietary": self.prop.cd,
            "Dt": strftime("%Y-%M-%d %H:%m:%s")
        }

    def sql(self, delimiter: str = ", ", br: bool = False) -> str:
        """

        """
        raw = self.__dict__()
        pool = []
        for k, v in raw.items():
            try:
                if k == "cd_client" and v > 0:
                    pool.append(f"{k} = {v}")
                elif k == "id_proprietry":
                    if type(v) is Proprietary:
                        pool.append(f"{k} = {v.cd}")
                    elif type(v) is int and v > 0:
                        pool.append(f"{k} = {v}")
                    else: continue
                elif k == "vl_root" and 2 > int(v) >= 0:
                    pool.append(f"{k} = {int(v)}")
                elif len(v) > 0 and v is not None:
                    pool.append(f"{k} = '{v}'")
                else: continue
            except TypeError: continue  # error treatment in case the len tries to count an int
        return delimiter.join(pool) + ";" if br else delimiter.join(pool)


class ClientsTable(Connection):
    """

    """

    def ls_clients(self) -> Tuple[Client]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        _cr = self.conn.cursor()
        rsp = _cr.execute("SELECT * FROM tb_clients;")
        clients = tuple([Client(x) for x in _cr.fetchall()])
        _cr.close()
        return clients

    def qr_client(self, cl: Client) -> Tuple[Client]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute("SELECT * FROM tb_clients WHERE " + cl.sql(" AND "))
        data = tuple([Client(x) for x in cursor.fetchall()])
        cursor.close()
        return data

    def id_getClient(self, id: int):
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute(f"SELECT * FROM tb_clients WHERE cd_client = {id}")
        cl  = cursor.fetchone()
        cursor.close()
        return Client(cl)
