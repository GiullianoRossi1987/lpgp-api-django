# encoding = UTF-8
# using namespace std
from ..connection.Connection import Connection
from typing import List, Tuple, Dict, AnyStr
from base64 import b64encode, b64decode
from datetime import datetime
from binascii import Error as B64Error


class Proprietary:
    """

    """

    cd: int = 0
    name: str = None
    email: str = None
    passwd: str = None
    img: str = None
    key: str = None
    checked: bool = None
    creation: datetime = None

    def __init__(self, lake = None):
        """

        """
        if type(lake) is list or type(lake) is tuple:
            self.cd = int(lake[0])
            self.name = str(lake[1])
            self.email = str(lake[2])
            self.passwd = str(lake[3])
            self.img = str(lake[4])
            self.key = str(lake[5])
            self.checked = True if int(lake[6]) == 1 else False
            self.creation = lake[7]
        elif type(lake) is dict:
            self.cd = int(lake["cd_proprietary"])
            self.name = str(lake["nm_proprietary"])
            self.email = str(lake["vl_email"])
            self.passwd = str(lake["vl_password"])
            self.img = str(lake["vl_img"])
            self.key = str(lake["vl_key"])
            self.checked = True if int(lake["checked"]) == 1 else False
            self.creation = lake["dt_creation"]
        else: pass

    def setData(self, lake):
        """

        """
        if type(lake) is list or type(lake) is tuple:
            self.cd = int(lake[0])
            self.name = str(lake[1])
            self.email = str(lake[2])
            self.passwd = str(lake[3])
            self.img = str(lake[4])
            self.key = str(lake[5])
            self.checked = True if int(lake[6]) == 1 else False
            self.creation = lake[7]
        elif type(lake) is dict:
            self.cd = int(lake["cd_proprietary"])
            self.name = str(lake["nm_proprietary"])
            self.email = str(lake["vl_email"])
            self.passwd = str(lake["vl_password"])
            self.img = str(lake["vl_img"])
            self.key = str(lake["vl_key"])
            self.checked = True if int(lake["checked"]) == 1 else False
            self.creation = lake["dt_creation"]
        else: raise TypeError("Invalid type of the data input, expecting list, tuple or dict")

    def __tuple__(self) -> tuple:
        """

        """
        return self.cd, self.name, self.email, self.passwd, self.img, self.key, self.checked, self.creation

    def __dict__(self) -> dict:
        """

        """
        return {
            "cd_proprietary": self.cd,
            "nm_proprietary": self.name,
            "vl_email": self.email,
            "vl_password": self.passwd,
            "vl_img": self.img,
            "vl_key": self.key,
            "checked": self.checked,
            "dt_creation": self.creation
        }

    def __str__(self):
        """
        """
        return ", ".join(map(lambda i: str(i), self.__tuple__()))

    def sql(self, sep = ",", break_seg: bool = True) -> str:
        """

        """
        raw = self.__dict__()
        pool = []
        for k, v in raw.items():
            try:
                if k == "cd_proprietary" and v > 0:
                    pool.append(f"{k} = {v}")
                elif k == "dt_creation" and (v is not None):
                    pool.append(f"{k} = '{str(v)}'")
                elif k == "checked" and 2 > v >= 0:
                    pool.append(f"{k} = {v}")
                elif len(v) > 0 and v is not None:
                    pool.append(f"{k} = '{v}'")
                else: continue
            except TypeError: continue  # error treatment in case the len tries to count an int
        return sep.join(pool) + ";" if break_seg else sep.join(pool)


class ProprietariesTable(Connection):
    """

    """

    class ProprietaryAuthenticationError(BaseException):
        """
        """

        def __init__(self, prp_cd: int):
            """
            """
            super(f"Authentication error on proprietary {prp_cd}")

    class ProprietaryNotFound(BaseException):
        """
        """

        def __init__(self, prp):
            """
            """
            super(f"There's no proprietary {prp}")

    class ProprietaryAlreadyExists(BaseException):
        """
        """

        def __init__(self, prp):
            """
            """
            super(f"The proprietary {prp} already exists")


    def propExists(self, prp: Proprietary) -> bool:
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute(f"SELECT cd_proprietary FROM tb_proprietaries WHERE cd_proprietary = {prp.cd};")
        ex = cursor.fetchone()[0]
        cursor.close()
        return ex == 1

    def ls_proprietaries(self) -> Tuple[Proprietary]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute("SELECT * FROM tb_proprietaries;")
        data = tuple([Proprietary(x) for x in cursor.fetchall()])
        cursor.close()
        return data

    def qr_proprietary(self, params: Proprietary) -> Tuple[Proprietary]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute("SELECT * FROM tb_proprietaries WHERE " + params.sql(" AND "))
        data = tuple([Proprietary(x) for x in cursor.fetchall()])
        cursor.close()
        return data


    def auth_proprietary(self, prop: Proprietary) -> bool:
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        if not self.propExists(prop): raise self.ProprietaryNotFound(prop.cd)
        compare = self.qr_proprietary(prop)[0]
        return compare.vl_key == prop.vl_key

    def auth_login(self, name: str, passwd: str) -> bool:
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute(f"SELECT * FROM tb_proprietaries WHERE nm_proprietary = \"{name}\";")
        res = cursor.fetchone()  # fetching only one 'cause the name is unique
        if len(res) == 0: raise self.ProprietaryNotFound(name)
        # tries to decode the password, to check if is encoded already or not
        macth = False
        try:
            _ = b64decode(passwd)
            # already encoded occasion
            match = res[3] == passwd
        except B64Error:
            match = res[3] == b64encode(passwd)
        return match

    def update_prop(self, old: Proprietary, new: Proprietary):
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        if not self.propExists(old.cd): raise self.ProprietaryNotFound(old.cd)
        cursor = self.conn.cursor()
        snew = new.sql(", ", False)
        rsp = cursor.execute(f"UPDATE FROM tb_proprietaries SET {snew} WHERE cd_proprietary = {old.cd};")
        cursor.close()
        return rsp

    def id_getProp(self, prp: int) -> Proprietary:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute(f"SELECT * FROM tb_proprietaries WHERE {prp};")
        prop = cursor.fetchone()
        cursor.close()
        return Proprietary(prop)
