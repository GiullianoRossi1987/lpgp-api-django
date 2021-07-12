# encoding = UTF-8
# using namespace std
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from lpgp.entities.Users import User, UsersTable
from lpgp.connection.Configurations import Configurations
from django.views.decorators.csrf import csrf_exempt
from util.default import val_client

@csrf_exempt
def index(request):
    """

    """
    if not val_client(request.POST["client-key"]):
        raise Exception("Invalid client")


    return render(request, "forbidden_err.html")
