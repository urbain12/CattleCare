from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #website
    path('',index,name='index'),
    path('Dashboard/',Dashboard,name='Dashboard'),
    path('logout/',logout,name='logout'),

    
    #Users
    path('Users/',Users,name='Users'),
    path('Operator/',Operator,name='Operator'),
    path('delete_user/<int:userID>/',delete_user,name="delete_user"),
    path('updateUser/<int:upID>/',updateUser,name="updateUser"),
    path('changeuserpassword/<int:userID>/',changeuserpassword,name="changeuserpassword"),

    #Vet
    path('Vet/',Vet,name='Vet'),
    path('addVet/',addVet,name='addVet'),


    #Hand
    path('Hand/',Hand,name='Hand'),
    path('addHand/',addHand,name='addHand'),

    #Breeder
    path('Breeder/',Breeder,name='Breeder'),
    path('addBreeder/',addBreeder,name='addBreeder'),

    #Case
    path('Cases/',Cases,name='Cases'),
    path('addCase/',addCase,name='addCase'),
    path('Reply/<int:caseID>/',Reply,name='Reply'),

    #Message
    path('Messages/',Messages,name='Messages'),
    path('addMessage/',addMessage,name='addMessage'),
    path('ReplyMsg/<int:MessageID>/',ReplyMsg,name='ReplyMsg'),

    #eport
    path('exportCsv/',exportCsv,name='exportCsv'),


    #Api
    path('breeder_login/',csrf_exempt(breeder_login),name='breeder_login'),
    path('change-password/', ChangePasswordView.as_view()),
    path('CreateCase/',CaseCreateView.as_view()),
    path('Casebyid/<int:user_id>/',Caselistbyid.as_view()),
    path('GetbreederbyId/<int:user_id>/',GetbreederbyId.as_view()),
]