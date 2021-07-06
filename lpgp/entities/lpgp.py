# encoding = utf-8
# using namespace std
from json import loads, dumps
from ..connection import Connection, Configurations
from .Proprietaries import Proprietary, ProprietariesTable
from .Signatures import Signature, SignaturesTable
from .Clients import ClientsTable, Client
from typing import AnyStr
from datetime import datetime
from .Controllers import Controller


class LPGPSignature:
    """

    """
    date_creation: datetime = None
    proprietary: Proprietary = None
    id: int = 0
    signature: str = ""
    dt_token: datetime = None
    __valid: bool = None

    @property
    def is_valid(self) -> bool:
        """
        """
        return self.__valid

    @staticmethod
    def decode(lpgp: str, delimiter: str = "/") -> dict:
        """

        """
        lpgp_s = lpgp.split(delimiter)
        json_d = ""
        for c in lpgp_s:
            json_d += chr(c)
        return loads(json_d)

    @staticmethod
    def encode(lpgp, delimiter: str = "/") -> LPGPSignature:
        """

        """
        con_a = []
        for l in lpgp: con_a.append(str(ord(l)))
        lpgp_e = delimiter.join(con_a)
        return LPGPSignature(lpgp_e)

    def authenticate(self):
        """

        """
        conf = Configurations("config.json")
        sig_t = SignaturesTable(conf)
        ctrl = Controller(conf)
        try:
            ext = sig_t.get_signature(self.id)
        except SignaturesTable.SignatureNotFound:
            self.__valid = False
        dre = ctrl.get_sd(self.dt_token)
        if len(dre) == 0: raise Controller.InvalidToken(self.dt_token)
        # Starts comparing
        bool_block = [
            ext.vl_password == self.signature,
            ext.prop_id == self.proprietary,
            dre["signature"] == self.id
        ]
        self.__valid = all(bool_block)


    def __init__(self, lake = None):
        """

        """
        if type(lake) is str:
            dct = LPGPSignature.decode(lake)
            self.date_creation = dct["Date-Creation"]
            self.proprietary = Proprietary()
            self.proprietary.cd = int(dct["Proprietary"])
            self.id = int(dct["ID"])
            self.signature = dct["Signature"]
            self.dt_token = dct["DToken"]
        elif type(lake) is dict:
            self.date_creation = lake["Date-Creation"]
            self.proprietary = Proprietary()
            self.proprietary.cd = int(lake["Proprietary"])
            self.id = int(lake["ID"])
            self.signature = lake["Signature"]
            self.dt_token = lake["DToken"]
        elif type(lake) is None or lake == None:
            pass
        else:
            raise TypeError("Invalid LPGP type")


class LPGPClient:
    """

    """

    client_pk: int = None
    prop_pk: int = None
    token = None
    date_creation: datetime = None
    download_tk: str = None

    path: AnyStr = None
    __readonly: bool = False

    class ReadonlyLockedData(BaseException):
        """

        """

        def __init__(self): super("Permission to change the data of the subject denied")

    @staticmethod
    def decode(content: str) -> dict:
        """

        """
        ascii_con = content.split("/")
        json_s = ""
        for char in ascii_con: json_s += chr(int(char))
        return json_loads(json_s)


    def __init__(self, **file_data):
        """

        """
        if "path" in file_data.keys() and "readonly" in file_data.keys():
            self.path = file_data["path"]
            self.__readonly = file_data["readonly"]
            # Loads from the file
            with open(file_data["path"], "r+") as conf_file:
                decoded = LPGPClient.decode(conf_file.read())
                self.client_pk = decoded["Client"]
                self.prop_pk = decoded["Proprietary"]
                self.token = decoded["Token"]
                self.date_creation = strptime(decoded["Dt"])
                self.download_tk = decoded["cdtk"]
        elif "key" in file_data.keys():
            data = LPGPClient.decode(file_data["key"])
            self.client_pk =  int(data["client"])
            self.prop_pk = int(data["proprietary"])
            self.token = data["token"]
            self.download_tk = data["download_tk"]
            self.date_creation = data["dt"]
        elif len(file_data) == 5:
            # Loads the direct data
            self.client_pk = file_data["client"].id if type(file_data["client"]) is Client else int(file_data["client"])
            self.prop_pk = file_data["proprietary"].id if type(file_data["proprietary"]) is Proprietary else int(file_data["proprietary"])
            # TODO: Turn it more legible
            self.token = file_data["token"]
            self.download_tk = file_data["download_tk"]
            self.date_creation = file_data["dt"]
        else: pass

    @property
    def client(self):
        """

        """
        if type(self.client_pk) is not None:
            conf = Configurations("config.json")
            t_cl = ClientsTable(conf)
            return t_cl.id_getClient(self.client_pk)
        return None

    @client.setter
    def client(self, new_data: Client):
        """

        """
        if self.__readonly: raise self.ReadonlyLockedData()
        else: self.client_pk = new_data.id

    @property
    def proprietary(self):
        """

        """
        if type(self.prop_pk) is not None:
            conf = Configurations("config.json")
            t_pr = ProprietariesTable(conf)
            return t_pr.id_getProp(self.prop_pk)
        return None

    @proprietary.setter
    def proprietary(self, ndata: Proprietary):
        """

        """
        if self.__readonly: raise self.ReadonlyLockedData()
        else: self.prop_pk = ndata.id

    @property
    def is_valid(self) -> bool:
        """

        """
        conf = Configurations("config.json")
        clt = ClientsTable(conf)
        ctrl = Controller(conf)
        try:
            ext = clt.id_getClient(self.client_pk)
        except:
            return False
        cre = ctrl.get_cd(self.download_tk)
        if len(cre) == 0: raise ctrl.InvalidToken(self.download_tk)
        return all([
            ext.token == self.token,
            ext.prop.id == self.prop_pk
        ])
