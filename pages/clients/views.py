# encoding = UTF-8
# using namespace std
# using @csfr_exempt

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from json import loads, dumps
from lpgp.connection.Connection import Connection
from lpgp.connection.Configurations import Configurations

@csrf_exempt
def index(request):
    """

    """
    conn = Connection(Configurations("config.json"))
    return JsonResponse({"teste": "conectado"})
