# encoding = UTF-8
# using namespace std
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from lpgp.connection.Configurations import Configurations
from lpgp.entities.Proprietaries import Proprietary, ProprietariesTable
from json import dumps
from lpgp.entities.lpgp import LPGPClient
from base64 import b64encode


def index(request):
    """

    """
    return render(request, "forbidden_err.html")

def val_client(client) -> bool:
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

@csrf_exempt
def login(request):
    """

    """
    try:
        if not val_client(request.POST["client-key"]):
            raise Exception("Invalid Client")
        prp_t = ProprietariesTable(Configurations("config.json"))
        paswd_r = request.POST["vl_password"] if request.POST["encoded"] == 't' else b64encode(request.POST["vl_password"].encode())
        if prp_t.auth_login(request.POST["nm_proprietary"], paswd_r):
            dct = {
                "status": 0,
                "response": "Login authenticated, valid"
            }
        else:
            dct = {
                "status": 2,
                "response": "Invalid login"
            }
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)

@csrf_exempt
def get(request):
    """

    """
    try:
        if not val_client(request.POST["client-key"]):
            raise Exception("Invalid Client")
        prp_t = ProprietariesTable(Configurations("config.json"))
        prp = Proprietary({k: i for k, i in request.POST.items()})
        req = prp_t.qr_proprietary(prp)
        if len(req) > 0:
            dct = {
                "status": 0,
                "response": tuple(x.__dict__() for x in req)
            }
        else:
            dct = {
                "status": 2,
                "response": "No proprietaries found"
            }
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)
