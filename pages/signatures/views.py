# encoding = UTF-8
# using namespace std
from lpgp.connection.Configurations import Configurations
from lpgp.entities.Signatures import Signature, SignaturesTable
from lpgp.entities.lpgp import LPGPSignature, LPGPClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from json import loads, dumps

sg_tb = SignaturesTable(Configurations("config.json"))

def index(request):
    """

    """
    return HttpResponse("Welcome to the cumzone")


def ls(request):
    """

    """
    try:
        dct = {
            "status": 0,
            "response": tuple( x.__dict__() for x in sg_tb.ls_signatures() )
        }
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)


def val_client(client) -> bool:
    """

    """
    try:
        lc = LPGPClient(key=client)
        if not lc.is_valid: raise Exception("Invalid Client Key")
        return True
        # DEBUG: raise Exception("Test error")
    except Exception as e:
        return False


@csrf_exempt
def auth(request):
    """

    """
    if not val_client(request.POST["client-key"]):
        raise Exception("Invalid client ")
    ls = LPGPSignature(request.POST["sig-key"])
    ls.authenticate()
    if ls.is_valid:
        dct = {
            "status": 0,
            "response": "Signature valid"
        }
    else:
        dct = {
            "status": 2,
            "response": "Invalid Signature"
        }
    return JsonResponse(dct)

@csrf_exempt
def get(request):
    """

    """
    try:
        if not val_client(request.POST["client-key"]):
            raise Exception("Invalid client ")
        if "key" in request.POST.keys():
            lc
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)