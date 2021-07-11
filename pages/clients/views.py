# encoding = UTF-8
# using namespace std
# using @csfr_exempt

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from json import loads, dumps
from lpgp.entities.Clients import ClientsTable, Client
from lpgp.connection.Configurations import Configurations
from lpgp.entities.lpgp import LPGPClient, LPGPSignature

conn = ClientsTable(Configurations("config.json"))

@csrf_exempt
def index(request):
    """

    """
    # TODO: add forbidden error page

@csrf_exempt
def ls(request):
    """

    """
    try:
        # DEBUG: raise Exception("Debug")
        dct = {
            "status": 0,
            "response": [x.__dict__() for x in conn.ls_clients()]
        }
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)

#DEBUG ONLY
@csrf_exempt
def ls_enc(request):
    """

    """
    try:
        # DEBUG: raise Exception("Debug")
        dct = {
            "status": 0,
            "response": [LPGPSignature.encode(x.__dict__()) for x in conn.ls_clients()]
        }
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)

@csrf_exempt
def val(request):
    """

    """
    try:
        lc = LPGPClient(key=request.POST["key"])
        if not lc.is_valid: raise Exception("Invalid Client Key")
        dct = {
            "status": 0,
            "response": f"OK, Client {lc.client_pk}"
        }
        # DEBUG: raise Exception("Test error")
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }

    return JsonResponse(dct)
