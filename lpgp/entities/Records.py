# encoding = UTF-8
# using namespace std
from ..connection.Connection import Connection
from ..connection.Configurations import Configurations
from typing import AnyStr, Tuple
from .Clients import Client
from datetime import datetime
from time import strftime, strptime

class ClientRecord:
    """

    """
    rec_id: int = None
    client_id: int = None
    dt_access: datetime = None
    success: bool = False

    def __init__(self, lake = None):
        """

        """
        if type(lake) is tuple or list:
            self.rec_id = lake[0]
            self.client_id = lake[1]
            self.dt_access = lake[2]
            self.success = bool(lake[3])
        elif type(lake) is dict:
            self.rec_id = lake["cd_access"]
            self.client_id = lake["id_client"]
            self.dt_access = lake["dt_access"]
            self.success = bool(lake["vl_success"])
        elif type(lake) is None: pass
        else: raise TypeError("Invalid lake type")

    def __dict__(self) -> dict:
        """

        """
        return {
            "cd_access": self.rec_id,
            "id_client": self.client_id,
            "dt_access": self.dt_access,
            "success": self.success
        }

    def sql(self, sep: str = ", ", br: bool = True) -> str:
        """

        """
        pool = []
        raw = self.__dict__()
        for k, v in raw.items():
            try:
                if (k == "cd_access" or k == "id_client") and v > 0:
                    pool.append(f"{k} = {v}")
                elif k == "dt_access" and (v is not None):
                    pool.append(f"{k} = '{str(v)}'")
                elif k == "vl_code" and Signature.check_code(v):
                    pool.append(f"{k} = {v}")
                elif len(v) > 0 and v is not None:
                    pool.append(f"{k} = '{v}'")
                else: continue
            except TypeError: continue  # error treatment in case the len tries to count an int
        return sep.join(pool) + ";" if br else sep.join(pool)

    def __tuple__(self) -> tuple:
        """

        """
        return self.rec_id, self.client_id, self.dt_access, self.success

    def __str__(self) -> str:
        """

        """
        return ", ".join(map(lambda i: str(i), self.__tuple__()))

class RecordsTable(Connection):
    """

    """

    class RecordNotFound(BaseException):
        """

        """

        def __init__(self, rec):
            super(f"Record '{rec}' not found")

    def ls_records(self) -> Tuple[ClientRecord]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cc = self.conn.cursor()
        rtr = cc.execute("SELECT * FROM tb_access;")
        data = tuple(ClientRecord(x) for x in cc.fetchall())
        cc.close()
        return data

    def __check_id(self, id) -> bool:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cc = self.conn.cursor()
        rtr = cc.execute("SELECT * FROM tb_access WHERE cd_access = %d;", (id.rec_id if type(id) is ClientRecord else int(id),))
        data = cc.fetchone()
        cc.close()
        return len(data) > 0

    def id_getRecord(self, id: int) -> ClientRecord:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        if not self.__check_id(id): raise self.RecordNotFound(id)
        cc = self.conn.cursor()
        rtr = cc.execute("SELECT * FROM tb_access WHERE cd_access = %d;", (id,))
        data = cc.fetchone()
        cc.close()
        return ClientRecord(data)

    def add_record(self, new_rec: ClientRecord):
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cc = self.conn.cursor()
        rtr = cc.execute("INSERT INTO tb_access (id_client, vl_success) VALUES (%d, %d);",
        (new_rec.client_id, int(new_rec.success)))
        cc.close()
