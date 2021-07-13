# encoding = utf-8
# using namespace std
from typing import Tuple, AnyStr
from ..connection.Configurations import Configurations
from ..connection.Connection import Connection
from base64 import b64encode, b64decode
from binascii import Error as B64Error
from datetime import datetime

class User:
    """

    """
    id: int            = None
    name: str          = None
    email: str         = None
    passwd: str        = None
    img: str           = None
    key: str           = None
    checked: bool      = None
    creation: datetime = None

    def __init__(self, lake = None):
        """

        """
        if type(lake) is list or type(lake) is tuple:
            self.id       = int(lake[0])
            self.name     = str(lake[1])
            self.email    = str(lake[2])
            self.passwd   = str(lake[3])
            self.img      = str(lake[4])
            self.key      = str(lake[5])
            self.checked  = bool(int(lake[6]))
            self.creation = lake[7]
        elif type(lake) is dict:
            self.id       = int(lake["cd_user"]) if "cd_user" in lake.keys() else None
            self.name     = str(lake["nm_user"]) if "cd_user" in lake.keys() else None
            self.email    = str(lake["vl_email"]) if "cd_user" in lake.keys() else None
            self.passwd   = str(lake["vl_password"]) if "cd_user" in lake.keys() else None
            self.img      = str(lake["vl_img"]) if "cd_user" in lake.keys() else None
            self.key      = str(lake["vl_key"]) if "cd_user" in lake.keys() else None
            self.checked  = bool(int(lake["checked"])) if "cd_user" in lake.keys() else None
            self.creation = lake["dt_creation"] if "cd_user" in lake.keys() else None
        elif lake == None or type(lake) is None: pass
        else: raise TypeError("Invalid type of data importing for user")

    def __tuple__(self) -> tuple:
        """

        """
        return self.id, self.name, self.email, self.passwd, self.img, self.key, self.checked, self.creation

    def __dict__(self) -> dict:
        """

        """
        return {
            "cd_user": self.id,
            "nm_user": self.name,
            "vl_email": self.email,
            "vl_password": self.passwd,
            "vl_img": self.img,
            "vl_key": self.key,
            "checed": self.checked,
            "dt_creation": self.creation
        }

    def __str__(self) -> str:
        """

        """
        return ", ".join(self.__tuple__())

    def sql(self, delimiter: str = ", ", br: bool = True) -> str:
        """

        """
        raw = self.__dict__()
        pool = []
        for k, v in raw.items():
            try:
                if k == "cd_user" and v > 0:
                    pool.append(f"{k} = {v}")
                elif k == "dt_creation" and (v is not None):
                    pool.append(f"{k} = '{str(v)}'")
                elif k == "checked" and 2 > v >= 0:
                    pool.append(f"{k} = {v}")
                elif len(v) > 0 and v is not None:
                    pool.append(f"{k} = '{v}'")
                else: continue
            except TypeError: continue  # error treatment in case the len tries to count an int
        return delimiter.join(pool) + ";" if br else delimiter.join(pool)


class UsersTable(Connection):
    """

    """

    class UserNotFoundError(BaseException):
        """

        """

        def __init__(self, usr):
            """

            """
            super(f"\"{usr}\" user not found in database")

    def user_exists(self, usr: User) -> bool:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute(f"SELECT cd_proprietary FROM tb_proprietaries WHERE cd_user = {usr.cd};")
        ex = cursor.fetchone()[0]
        cursor.close()
        return ex == 1

    def ls_users(self) -> Tuple[User]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute("SELECT * FROM tb_users;")
        data = tuple([User(x) for x in cursor.fetchall()])
        cursor.close()
        return data

    def qr_user(self, usr: User) -> Tuple[User]:
        """

        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute("SELECT * FROM tb_proprietaries WHERE " + usr.sql(" AND "))
        data = tuple([Proprietary(x) for x in cursor.fetchall()])
        cursor.close()
        return data

    def auth_proprietary(self, usr: User) -> bool:
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        if not self.user_exists(usr): raise self.UserNotFoundError(usr.cd)
        compare = self.qr_user(usr)[0]
        return compare.vl_key == usr.vl_key

    def auth_login(self, name: str, passwd: str) -> bool:
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        cursor = self.conn.cursor()
        rsp = cursor.execute(f"SELECT * FROM tb_users WHERE nm_user = \"{name}\";")
        res = cursor.fetchone()  # fetching only one 'cause the name is unique
        if len(res) == 0: raise self.UserNotFoundError(name)
        # tries to decode the password, to check if is encoded already or not
        macth = False
        try:
            _ = b64decode(passwd)
            # already encoded occasion
            match = res[3] == passwd.decode()
        except B64Error:
            match = res[3] == b64encode(passwd)
        return match

    def update(self, old: User, new: User):
        """
        """
        if not self.is_connected: raise self.NotConnectedError()
        if not self.user_exists(old.cd): raise self.User(old.cd)
        cursor = self.conn.cursor()
        snew = new.sql(", ", False)
        rsp = cursor.execute(f"UPDATE FROM tb_users SET {snew} WHERE cd_user = {old.cd};")
        cursor.close()
        return rsp
