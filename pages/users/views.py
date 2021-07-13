# encoding = UTF-8
# using namespace std
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from lpgp.entities.Users import User, UsersTable
from lpgp.connection.Configurations import Configurations
from django.views.decorators.csrf import csrf_exempt
from util.default import val_client
from base64 import b64encode

def index(request):
    """

    """
    return render(request, "forbidden_err.html")

@csrf_exempt
def login(request):
    """

    """
    try:
        if not val_client(request.POST["client-key"]):
            raise Exception("Invalid Client")
        usr_t = UsersTable(Configurations("config.json"))
        paswd_r = request.POST["password"] if request.POST["encoded"] == "t" else b64encode(request.POST["password"].encode())
        if usr_t.auth_login(request.POST["name"], paswd_r):
            dct = {
                "status": 0,
                "response": "OK, valid user"
            }
        else:
            dct = {
                "status": 2,
                "response": "Ok, invalid user"
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
        usr_t = UsersTable(Configurations("config.json"))
        usr_r = User({k: v for k, v in request.POST.items()})
        dct = {
            "status": 0,
            "response": tuple(x.__dict__() for x in usr_t.qr_user(usr_r))
        }
    except Exception as e:
        dct = {
            "status": 1,
            "response": str(e)
        }
    return JsonResponse(dct)
