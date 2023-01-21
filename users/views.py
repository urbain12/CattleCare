from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
from django.db.models import Q
import threading
# from .utils import cartData, check_transaction, check_instalment
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .models import *
import secrets
import string



# from dateutil.relativedelta import *
from django.contrib.auth import (
    authenticate,
    logout as django_logout,
    login as django_login,
)
from django.shortcuts import render, redirect
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core import serializers
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta
import json
from django.contrib import messages
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
import os
import csv
from twilio.rest import Client
# Create your views here.
def index(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST["email"], password=request.POST["password"]
        )
        if customer is not None:
            django_login(request, customer)
            return redirect("Dashboard")
        else:
            return render(
                request,
                "Login.html",
                {"error": "Your Email or Password are incorrect. "},
            )
    else:
        return render(request, 'Login.html')

@login_required(login_url="/login")
def logout(request):
    django_logout(request)
    return redirect("index")

def Dashboard(request):
    allHand = len(User.objects.filter(typee = 'Hand'))
    allVet = len(User.objects.filter(typee = 'Vet'))
    allcat = len(User.objects.filter(typee = 'Breeder'))
    return render(request, 'Dashboard.html',{
            "allHand": allHand,
            "allVet": allVet,
            "allcat": allcat,
        })

#Users
def Operator(request):
    if request.method == "POST":
        try:
            user1 = User.objects.get(email=request.POST["email"])
            return render(
                request, "Operator.html", {"error": "The Email  has already been taken"}
            )
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST["phone"])
                return render(
                    request,
                    "Operator.html",
                    {"error": "The phone number  has already been taken"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.POST["fname"],
                    LastName=request.POST["lname"],
                    Province=request.POST["Pname"],
                    District=request.POST["Dname"],
                    Sector=request.POST["Sname"],
                    Cell=request.POST["Cname"],
                    typee=request.POST["Utype"],
                    email=request.POST["email"],
                    phone=request.POST["phone"],
                    password=request.POST["pswd"],
                )
            return redirect("Users")
    else:
        return render(request, 'Operator.html')

def Users(request):
    Admin=User.objects.filter(typee='Admin')
    return render(request, 'Users.html',{'Admin':Admin})

@login_required(login_url="/login")
def updateUser( request, upID):
    updateuser = User.objects.get(id=upID)
    if request.method == "POST":
        updateuser.FirstName = request.POST["fname"]
        updateuser.LastName = request.POST["lname"]
        updateuser.Province = request.POST["Pname"]
        updateuser.District = request.POST["Dname"]
        updateuser.Sector = request.POST["Sname"]
        updateuser.Cell = request.POST["Cname"]
        updateuser.email = request.POST["email"]
        updateuser.phone = request.POST["phone"]
        updateuser.save()
        return redirect("Users")
    else:
        return render(request, "updateUsers.html", {"updateuser": updateuser})


def delete_user(request, userID):
    user = User.objects.get(id=userID)
    user.delete()
    return redirect("Users")

@login_required(login_url='/login')
def changeuserpassword(request, userID):
    if request.method == 'POST':
        if request.POST['newpassword'] == request.POST['confirmpassword']:
            user = User.objects.get(id=userID)
            if user.check_password(request.POST['password']):
                password = request.POST['newpassword']
                user.set_password(password)
            user.save()
            return redirect('Users')
        else:
            alert = True
            return render(request, 'changepassword.html', {'alert': alert})
    else:
        alert = False
        return render(request, 'changepassword.html', {'alert': alert})

#Vet
def Vet(request):
    Vete=User.objects.filter(typee='Vet')
    sec=User.objects.values('Sector').distinct()
    print(sec)
    return render(request, 'Vetenary.html',{'Vete':Vete,'sec':sec})

def addVet(request):
    if request.method == "POST":
        try:
            user1 = User.objects.get(email=request.POST["email"])
            return render(
                request, "operator.html", {"error": "The Email  has already been taken"}
            )
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST["phone"])
                return render(
                    request,
                    "Operator.html",
                    {"error": "The phone number  has already been taken"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.POST["fname"],
                    LastName=request.POST["lname"],
                    Province=request.POST["Pname"],
                    District=request.POST["Dname"],
                    Sector=request.POST["Sname"],
                    Cell=request.POST["Cname"],
                    typee="Vet",
                    email=request.POST["email"],
                    phone=request.POST["phone"],
                    password=request.POST["pswd"],
                )
            return redirect("Vet")
    else:
        return render(request, 'addVet.html')





#hand
def Hand(request):
    Hands=User.objects.filter(typee='Hand')
    return render(request, 'Hand.html',{'Hands':Hands})

def addHand(request):
    if request.method == "POST":
        try:
            user1 = User.objects.get(email=request.POST["email"])
            return render(
                request, "operator.html", {"error": "The Email  has already been taken"}
            )
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST["phone"])
                return render(
                    request,
                    "Operator.html",
                    {"error": "The phone number  has already been taken"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.POST["fname"],
                    LastName=request.POST["lname"],
                    Province=request.POST["Pname"],
                    District=request.POST["Dname"],
                    Sector=request.POST["Sname"],
                    Cell=request.POST["Cname"],
                    typee="Hand",
                    email=request.POST["email"],
                    phone=request.POST["phone"],
                    password=request.POST["pswd"],
                )
            return redirect("Hand")
    else:
        return render(request, 'addHand.html')
#Breeder

def Breeder(request):
    breeder=User.objects.filter(typee='Breeder')
    return render(request, 'Breeder.html',{'breeder':breeder})

def addBreeder(request):
    if request.method == "POST":
        try:
            user1 = User.objects.get(email=request.POST["email"])
            return render(
                request, "operator.html", {"error": "The Email  has already been taken"}
            )
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST["phone"])
                return render(
                    request,
                    "Operator.html",
                    {"error": "The phone number  has already been taken"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.POST["fname"],
                    LastName=request.POST["lname"],
                    Province=request.POST["Pname"],
                    District=request.POST["Dname"],
                    Sector=request.POST["Sname"],
                    Cell=request.POST["Cname"],
                    typee="Breeder",
                    email=request.POST["email"],
                    phone=request.POST["phone"],
                    password=request.POST["pswd"],
                )
            return redirect("Breeder")
    else:
        return render(request, 'addBreeder.html')

#Message
def Cases(request):
    cases=Case.objects.filter(Sector =request.user.Sector)
    return render(request, 'Cases.html',{'cases':cases})

def addCase(request):
    if request.method == "POST":
        user=User.objects.get(id=request.POST['cid'])
        AddCase = Case()
        AddCase.user=user
        AddCase.symptoms = request.POST["symptom"]
        AddCase.cattleType = request.POST["Ctype"]
        AddCase.image = request.FILES['images']
        AddCase.Sector = request.user.Sector
        AddCase.Message = request.POST["Msg"]
        AddCase.save()
        return redirect("Cases")
    else:
        users=User.objects.filter(typee='Breeder')
        return render(request, 'addCase.html',{'users':users})

def Reply(request,caseID):
    if request.method == 'POST':
        print('replyreply reply')
        req = Case.objects.only('id').get(
            id=caseID)
        req.reply = request.POST['Msg']
        req.replied = True
        req.save()
        return redirect('Cases')
    else:
        case = Case.objects.get(id=caseID)
        return render(request, 'replycase.html',{"case":case})


#Message
def Messages(request):
    messages=Message.objects.filter(Sector =request.user.Sector)
    return render(request, 'Message.html',{'messages':messages})

def addMessage(request):
    if request.method == "POST":
        user=User.objects.get(id=request.POST['cid'])
        AddMessage = Message()
        AddMessage.user=user
        AddMessage.Sector = request.user.Sector
        AddMessage.Message = request.POST["Msg"]
        AddMessage.save()
        return redirect("Messages")
    else:
        users=User.objects.filter(typee='Vet')
        return render(request, 'addMessage.html',{'users':users})

def ReplyMsg(request,MessageID):
    if request.method == 'POST':
        print('replyreply reply')
        req = Message.objects.only('id').get(
            id=MessageID)
        req.reply = request.POST['Msg']
        req.replied = True
        req.save()
        return redirect('Messages')
    else:
        msg=Message.objects.get(id=MessageID)
        return render(request, 'replyMessage.html',{"msg":msg})



#ExportCSV

def exportCsv(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    start=request.POST['start']
    end=request.POST['end']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Case from {start} to {end} Vaccine Report - {ondate}.csv"'
    writer = csv.writer(response)
    writer.writerow([

        'RVF CATTLE CARE'
    ])
    
    writer.writerow([

        "Range"+' : '+start+'-'+end

    ])
   
    
    
                    
    cases = Case.objects.filter(send_at__range=[request.POST['start'],request.POST['end']])    
    instalments = []
    for sub in cases:
            transactions = [
                sub.user.FirstName+" "+sub.user.LastName,
                sub.Message,
                sub.symptoms,
                sub.cattleType,
                sub.reply,
                sub.send_at,
            ]

            print(transactions)
            print(type(transactions))
            instalments.append(transactions)

    writer.writerow([
        "Number of cases: " + str(len(instalments))

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Breeder Names','Case','Symptoms','CattleType','Reply','send date' ])
    for user in instalments:
        writer.writerow(user)

    return response




def exportVet(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    vets=request.POST['vet']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="List of vet - {ondate}.csv"'
    writer = csv.writer(response)
    writer.writerow([

        'RVF CATTLE CARE'
    ])

    writer.writerow([

        {vets}

    ])
     
                    
    Vet = User.objects.filter(Sector = request.POST['vet'], typee='Vet')    
    instalments = []
    for sub in Vet:
            transactions = [
                sub.FirstName+" "+sub.LastName,
                sub.Sector,
                sub.Cell,
                sub.phone,
                sub.email,
            ]

            print(transactions)
            print(type(transactions))
            instalments.append(transactions)

    writer.writerow([
        "Number of Vet: " + str(len(instalments))

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Vet Names','Sector','Cell','phone','email'])
    for user in instalments:
        writer.writerow(user)

    return response


def exportHand(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="List of Hand - {ondate}.csv"'
    writer = csv.writer(response)
    writer.writerow([

        'RVF CATTLE CARE'
    ])

    writer.writerow([

        {request.user.Sector}

    ])
     
                    
    Vet = User.objects.filter(Sector = request.user.Sector, typee='Hand')    
    instalments = []
    for sub in Vet:
            transactions = [
                sub.FirstName+" "+sub.LastName,
                sub.Sector,
                sub.Cell,
                sub.phone,
                sub.email,
            ]

            print(transactions)
            print(type(transactions))
            instalments.append(transactions)

    writer.writerow([
        "Number of Vet: " + str(len(instalments))

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Vet Names','Sector','Cell','phone','email'])
    for user in instalments:
        writer.writerow(user)

    return response


def exportBreeder(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="List of Breeder - {ondate}.csv"'
    writer = csv.writer(response)
    writer.writerow([

        'RVF CATTLE CARE'
    ])

    writer.writerow([

        {request.user.Sector}

    ])
     
                    
    Vet = User.objects.filter(Sector = request.user.Sector, typee='Breeder')    
    instalments = []
    for sub in Vet:
            transactions = [
                sub.FirstName+" "+sub.LastName,
                sub.Sector,
                sub.Cell,
                sub.phone,
                sub.email,
            ]

            print(transactions)
            print(type(transactions))
            instalments.append(transactions)

    writer.writerow([
        "Number of Vet: " + str(len(instalments))

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Vet Names','Sector','Cell','phone','email'])
    for user in instalments:
        writer.writerow(user)

    return response

#Mobile

def breeder_login(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(phone=body["phone"])
            if user.check_password(body["password"]):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "status": "success",
                    "token": str(token),
                    "code": status.HTTP_200_OK,
                    "message": "Kwinjira byagenze neza",
                    "data": [],
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json")
            else:
                data = {
                    "status": "failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Phone or password incorrect!",
                    "data": [],
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json")
        except User.DoesNotExist:
            data = {
                "status": "failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Phone or password incorrect!",
                "data": [],
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type="application/json")


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.data["user_id"])
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password ChangePasswupdated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CaseCreateView(CreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class Caselistbyid(ListAPIView):
    serializer_class = CaseSerializer
    
    def get_queryset(self):
        return Case.objects.filter(user=self.kwargs['user_id'])

class GetbreederbyId(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['user_id'])




