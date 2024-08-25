from django.urls import path
from .views import *

urlpatterns = [
    path("", login, name="login"),
    path("teams/<str:pk>/", teams, name="teams"),
    path(
        "courseOutline/<str:pk>/<str:sk>/", courseOutline, name="courseOutline"
    ),
    path(
        "recordOfInvention/<str:pk>/<str:sk>/",
        recordOfInvention,
        name="recordOfInvention",
    ),
    path(
        "statementOfOriginality/<str:pk>/<str:sk>/<str:tk>/<str:fk>",
        statementOfOriginality,
        name="statementOfOriginality",
    ),  
    path("deleteInfo/<str:pk>/<str:sk>/<str:tk>/<str:fk>", deleteInfo, name="deleteInfo"),
    path("editInfo/<str:pk>/<str:sk>/<str:tk>/<str:fk>", editInfo, name="editInfo"),
    path("flowchart/<str:pk>/<str:sk>/", flowchart, name="flowchart"),
    path("stepOne/<str:pk>/<str:sk>/", stepOne, name="stepOne"),
    path("stepTwoOne/<str:pk>/<str:sk>/", stepTwoOne, name="stepTwoOne"),
    path("stepTwoTwo/<str:pk>/<str:sk>/", stepTwoTwo, name="stepTwoTwo"),
    path("stepTwoThree/<str:pk>/<str:sk>/", stepTwoThree, name="stepTwoThree"),
    path("stepTwoFour/<str:pk>/<str:sk>/", stepTwoFour, name="stepTwoFour"),
    path("stepThreeOne/<str:pk>/<str:sk>/", stepThreeOne, name="stepThreeOne"),
    path("stepThreeTwo/<str:pk>/<str:sk>/", stepThreeTwo, name="stepThreeTwo"),
    path("stepThreeThree/<str:pk>/<str:sk>/", stepThreeThree, name="stepThreeThree"),
    path("stepFourOne/<str:pk>/<str:sk>/", stepFourOne, name="stepFourOne"),
    path("stepFourTwo/<str:pk>/<str:sk>/", stepFourTwo, name="stepFourTwo"),
    path("stepFiveOne/<str:pk>/<str:sk>/", stepFiveOne, name="stepFiveOne"),
    path("stepFiveTwo/<str:pk>/<str:sk>/", stepFiveTwo, name="stepFiveTwo"),
    path("stepSix/<str:pk>/<str:sk>/", stepSix, name="stepSix"),
    path('viewImage/<int:pk>/', viewImage, name='viewImage'),
    path("stepSeven/<str:pk>/<str:sk>/", stepSeven, name="stepSeven"),
    path("guidelines/<str:pk>/<str:sk>/", guidelines, name="guidelines"),
    path("stepEightOne/<str:pk>/<str:sk>/", stepEightOne, name="stepEightOne"),
    path("stepEightTwo/<str:pk>/<str:sk>/", stepEightTwo, name="stepEightTwo"),
    path("stepEightThree/<str:pk>/<str:sk>/", stepEightThree, name="stepEightThree"),
    path("notes/<str:pk>/<str:sk>/", notes, name="notes"),
    path("previewLogbook/<str:pk>/<str:sk>/", previewLogbook, name="previewLogbook"),
    path("survey/<str:pk>/<str:sk>/", survey, name="survey"),
]
