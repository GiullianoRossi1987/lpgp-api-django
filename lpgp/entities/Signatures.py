# encoding = UTF-8
# using namespace std
from ..connection.Connection import Connection, Configurations
from typing import AnyStr
from datetime import datetime
from hashlib import md5, sha256, sha1
from typing import List, Tuple, Dict
from .Proprietaries import Proprietary, ProprietariesTable


class Signature:
    id: int = 0
    prop_id: int = 0
    code: int = None
    vl_password: str = None
    dt_creation: datetime = None

    # Exceptions
    class InvalidCode(BaseException):
        """

        """

        def __init__(self, code: int):
            """

            """
            super(f"The code {code} isn't a valid signature code")

    @staticmethod
    def check_code(code: int) -> bool:
        """

        """
        return code in (0, 1, 2)

    @staticmethod
    def encode(content: str, code: int):
        """

        """
        if code in (0, 1, 2):
            if code == 0:
                return str(md5(content))
            elif code == 1:
                return str(sha1(content))
            else:
                return str(sha256(content))
        else:
            return None

    def __init__(self, lake = None):
        """

        """
        # checks the code
        if type(lake) is tuple or type(lake) is list:
            if not self.check_code(lake[2]):
                raise self.InvalidCode(lake[2])
            self.id = lake[0]
            self.prop_id = lake[1]
            self.code = lake[2]
            self.vl_password = lake[3]
            self.dt_creation = lake[4]
        elif type(lake) is dict:
            if not self.check_code(lake["vl_code"]):
                raise self.InvalidCode(lake["vl_code"])
            self.id = lake["cd_signature"]
            self.prop_id = lake["id_proprietary"]
            self.code = lake["vl_code"]
            self.vl_password = lake["vl_password"]
            self.dt_creation = lake["dt_creation"]
        elif type(lake) is None or lake == None: pass
        else:
            raise RuntimeError("Invalid type to convert")

    @property
    def proprietary(self) -> Proprietary:
        """

        """
        c = Configurations("config.json")
        t_prop = ProprietariesTable(c)
        l_prop = Proprietary()
        l_prop.cd = self.prop_id
        return t_prop.qr_proprietary(l_prop)[0]

    def __dict__(self) -> dict:
        """

        """
        return {
            "cd_signature": self.id,
            "id_proprietary": self.prop_id,
            "vl_code": self.code,
            "vl_password": self.vl_password,
            "dt_creation": self.dt_creation
        }

    def __tuple__(self) -> tuple:
        """

        """
        return self.id, self.prop_id, self.code, self.vl_password, self.dt_creation

    def __str__(self) -> str:
        """

        """
        return ", ".join(self.__tuple__())

    def sql(self, sep: str = ", ", br: bool = True) -> str:
        """

        """
        pool = []
        raw = self.__dict__()
        for k, v in raw.items():
            try:
                if (k == "cd_signature" or k == "cd_proprietary") and v > 0:
                    pool.append(f"{k} = {v}")
                elif k == "dt_creation" and (v is not None):
                    pool.append(f"{k} = '{str(v)}'")
                elif k == "vl_code" and Signature.check_code(v):
                    pool.append(f"{k} = {v}")
                # elif k == "checked" and 2 > v >= 0:
                #     pool.append(f"{k} = {v}")
                elif len(v) > 0 and v is not None:
                    pool.append(f"{k} = '{v}'")
                else: continue
            except TypeError: continue  # error treatment in case the len tries to count an int
        return sep.join(pool) + ";" if br else sep.join(pool)

class SignaturesTable(Connection):
    """

    """

    class SignatureNotFound(BaseException):
        """

        """

        def __init__(self, sig):
            """

            """
            super(f"\"{sig}\" signature not found")

    def signature_exists(self, sig) -> bool:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cr = self.conn.cursor()
        if type(sig) is int:
            r1 = cr.execute(f"SELECT cd_signature FROM tb_signatures WHERE cd_signature = {sig}")
            r2 = len(cr.fetchall()) == 1
            cr.close()
            return r2
        elif type(sig) is Signature:
            return self.signature_exists(sig.cd)
        else: raise TypeError("Invalid reference type for signature")


    def ls_signatures(self) -> Tuple[Signature]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cr = self.conn.cursor()
        rsp = cr.execute("SELECT * FROM tb_signatures;")
        rt = tuple([Signature(x) for x in cr.fetchall()])
        cr.close()
        return rt

    def get_signature(self, id: int) -> Signature:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        if not self.signature_exists(id): raise self.SignatureNotFound(id)
        cr = self.conn.cursor()
        rsp = cr.execute("SELECT * FROM tb_signatures WHERE cd_signature = %s", (int(id), ))
        r = cr.fetchone()
        cr.close()
        return Signature(r)

    def qr_signature(self, params: Signature) -> Tuple[Signature]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cr = self.conn.cursor()
        qr = params.sql(" AND ")
        rso = cr.execute(f"SELECT * FROM tb_signatures WHERE {qr}")
        r = cr.fetchall()
        cr.close()
        return tuple([Signature(x) for x in r])
