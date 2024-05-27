from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="home"),
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
    # path("stepFour/<str:pk>/<str:sk>/", views.stepFour, name="stepFour"),
    # path("step_5/<str:pk>/<str:sk>/", views.step_5, name="step_5"),
    
]
