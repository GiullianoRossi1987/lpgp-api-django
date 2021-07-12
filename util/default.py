# encoding = UTF-8
# using namespace std
from os.path import join as path_join
from lpgp_api_django.settings import BASE_DIR
from lpgp.entities.lpgp import LPGPClient
from lpgp.entities.Records import ClientRecord, RecordsTable
from lpgp.connection.Configurations import Configurations
from datetime import datetime
from time import strptime

BOOTSTRAP_PATH = path_join(BASE_DIR, "util/bootstrap")

def val_client(client) -> bool:
    """

    """
    rcn = ClientRecord()
    try:
        rct = RecordsTable(Configurations("config.json"))
        lc = LPGPClient(key=client)
        # lc.authenticate()
        with open("logs/debug.log", "w") as dbg:
            dbg.write(str(lc.client_pk))
        rcn.client_id = lc.client_pk
        # rcn.dt_access = strptime("%Y-%M-%d %H:%m:%s")
        if not lc.is_valid:
            rcn.success = False
            # raise Exception("Invalid Client Key")
        rcn.success = True
        # return True
        # DEBUG: raise Exception("Test error")
    except Exception as e:
        rcn.success = False
    rct.add_record(rcn)
    return rcn.success


def val_client_na(client) -> bool:
    """

    """
    try:
        lc = LPGPClient(key=client)
        # lc.authenticate()
        if not lc.is_valid: raise Exception("Invalid Client Key")
        return True
        # DEBUG: raise Exception("Test error")
    except Exception as e:
        return False
