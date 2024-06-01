from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("teams/<str:pk>/", views.teams, name="teams"),
    path(
        "courseOutline/<str:pk>/<str:sk>/", views.courseOutline, name="courseOutline"
    ),
    path(
        "recordOfInvention/<str:pk>/<str:sk>/",
        views.recordOfInvention,
        name="recordOfInvention",
    ),
    path(
        "statementOfOriginality/<str:pk>/<str:sk>/",
        views.statementOfOriginality,
        name="statementOfOriginality",
    ),
    path("flowchart/<str:pk>/<str:sk>/", views.flowchart, name="flowchart"),
    path("stepOne/<str:pk>/<str:sk>/", views.stepOne, name="stepOne"),
    path("stepTwoOne/<str:pk>/<str:sk>/", views.stepTwoOne, name="stepTwoOne"),
    path("stepTwoTwo/<str:pk>/<str:sk>/", views.stepTwoTwo, name="stepTwoTwo"),
    path("stepTwoThree/<str:pk>/<str:sk>/", views.stepTwoThree, name="stepTwoThree"),
    path("stepTwoFour/<str:pk>/<str:sk>/", views.stepTwoFour, name="stepTwoFour"),
    path("stepThreeOne/<str:pk>/<str:sk>/", views.stepThreeOne, name="stepThreeOne"),
    path("stepThreeTwo/<str:pk>/<str:sk>/", views.stepThreeTwo, name="stepThreeTwo"),
    path("stepThreeThree/<str:pk>/<str:sk>/", views.stepThreeThree, name="stepThreeThree"),
    path("stepFourOne/<str:pk>/<str:sk>/", views.stepFourOne, name="stepFourOne"),
    path("stepFourTwo/<str:pk>/<str:sk>/", views.stepFourTwo, name="stepFourTwo"),
    path("stepFiveOne/<str:pk>/<str:sk>/", views.stepFiveOne, name="stepFiveOne"),
    path("stepFiveTwo/<str:pk>/<str:sk>/", views.stepFiveTwo, name="stepFiveTwo"),
    path("stepSix/<str:pk>/<str:sk>/", views.stepSix, name="stepSix"),
    path('view/<int:pk>/', views.view_image, name='view_image'),
    path("stepSeven/<str:pk>/<str:sk>/", views.stepSeven, name="stepSeven"),
    path("guidelines/<str:pk>/<str:sk>/", views.guidelines, name="guidelines"),
    path("stepEightOne/<str:pk>/<str:sk>/", views.stepEightOne, name="stepEightOne"),
    path("stepEightTwo/<str:pk>/<str:sk>/", views.stepEightTwo, name="stepEightTwo"),
    path("stepEightThree/<str:pk>/<str:sk>/", views.stepEightThree, name="stepEightThree"),
    
]
