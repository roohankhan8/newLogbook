from django.db import connections
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from website.utils import has_data_changed
from .forms import *
from .models import *

# Create your views here.

def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = "Student"
        with connections["user_database"].cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tbl_user WHERE email=%s AND password=%s AND user_type=%s",
                [email, password, user_type],
            )
            user_data = cursor.fetchone()
        if user_data:
            return redirect("teams", user_data[0])
        else:
            messages.error(request, "Username or Password is incorrect!")
            return render(request, "login.html", {"error": "Invalid login credentials"})
    return render(request, "login.html")


def teams(request, pk):
    student_id = pk
    with connections["user_database"].cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tbl_team_member WHERE student_id=%s", [student_id]
        )
        user_data = cursor.fetchall()
    team_ids = []
    all_teams = []
    teams = {}
    if user_data:
        for i in user_data:
            team_ids.append(i[1])
        for i in team_ids:
            with connections["user_database"].cursor() as cursor:
                cursor.execute("SELECT * FROM tbl_team WHERE id=%s", [i])
                team_data = cursor.fetchone()
                all_teams.append(team_data)
        for i in all_teams:
            teams[i[0]] = i[1]
    context = {"pk": pk, "user": user_data, "teams": teams}
    return render(request, "teams.html", context)


def courseOutline(request, pk, sk):
    student_id = pk
    team_id = sk
    with connections["user_database"].cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tbl_team_member WHERE student_id=%s", [student_id]
        )
        user_data = cursor.fetchone()
        # print(user_data)
    with connections["user_database"].cursor() as cursor:
        cursor.execute("SELECT * FROM tbl_team WHERE id=%s", [team_id])
        team_data = cursor.fetchone()
    context = {"pk": pk, "sk": sk, "user": user_data, "team": team_data}
    return render(request, "outline.html", context)


def flowchart(request, pk, sk):
    if request.method == "POST":
        return redirect("step_1", pk, sk)
    context = {"pk": pk, "sk": sk}
    return render(request, "flowchart.html", context)


def recordOfInvention(request, pk, sk):
    record = (
        RecordOfInvention.objects.filter(teamId=sk).order_by("-date_updated").first()
    )
    form = RecordOfInventionForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            new_record = RecordOfInvention(userId=pk, teamId=sk, **form.cleaned_data)
            new_record.save()
            return redirect("statementOfOriginality", pk, sk)
    context = {"form": form}
    return render(request, "recordOfInvention.html", context)


def statementOfOriginality(request, pk, sk):
    statement = (
        StatementOfOriginality.objects.filter(teamId=sk)
        .order_by("-date_updated")
        .first()
    )
    if request.method == "POST":
        action = request.POST.get("action")
        inventor1 = request.POST.get("inventor1")
        schoolnamegrade1 = request.POST.get("schoolnamegrade1")
        sig1 = request.POST.get("sig1")
        date1 = request.POST.get("date1")
        inventor2 = request.POST.get("inventor2")
        schoolnamegrade2 = request.POST.get("schoolnamegrade2")
        sig2 = request.POST.get("sig2")
        date2 = request.POST.get("date2")
        inventor3 = request.POST.get("inventor3")
        schoolnamegrade3 = request.POST.get("schoolnamegrade3")
        sig3 = request.POST.get("sig3")
        date3 = request.POST.get("date3")
        inventor4 = request.POST.get("inventor4")
        schoolnamegrade4 = request.POST.get("schoolnamegrade4")
        sig4 = request.POST.get("sig4")
        date4 = request.POST.get("date4")
        inventor5 = request.POST.get("inventor5")
        schoolnamegrade5 = request.POST.get("schoolnamegrade5")
        sig5 = request.POST.get("sig5")
        date5 = request.POST.get("date5")
        inventor1 = Inventor.objects.create(
            inventor=inventor1, schoolnamegrade=schoolnamegrade1, sig=sig1, date=date1
        )
        inventor2 = Inventor.objects.create(
            inventor=inventor2, schoolnamegrade=schoolnamegrade2, sig=sig2, date=date2
        )
        inventor3 = Inventor.objects.create(
            inventor=inventor3, schoolnamegrade=schoolnamegrade3, sig=sig3, date=date3
        )
        inventor4 = Inventor.objects.create(
            inventor=inventor4, schoolnamegrade=schoolnamegrade4, sig=sig4, date=date4
        )
        inventor5 = Inventor.objects.create(
            inventor=inventor5, schoolnamegrade=schoolnamegrade5, sig=sig5, date=date5
        )
        statement_of_originality_instance = StatementOfOriginality.objects.create(
            userId=pk,
            teamId=sk,
        )
        statement_of_originality_instance.inventors.add(
            inventor1, inventor2, inventor3, inventor4, inventor5
        )
        if action == "save":
            return HttpResponseRedirect(request.path_info)
        elif action == "next":
            return redirect("flowchart", pk=pk, sk=sk)
    if statement:
        context = {
            "pk": pk,
            "sk": sk,
            "statement": statement,
            "inventors": statement.inventors.all,
        }
    else:
        context = {"pk": pk, "sk": sk, "statement": statement}
    return render(request, "statementOfOriginality.html", context)


def stepOne(request, pk, sk):
    step1 = StepOne.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        identify_problems = request.POST.get("identify_problems")
        if action in ('next', 'add') and identify_problems!='':
            new_problem = StepOne.objects.create(userId=pk, teamId=sk)
            new_problem.identify_problems = identify_problems
            new_problem.save()
            if action == 'add':
                return HttpResponseRedirect(request.path_info)        
            elif action == "next":
                return redirect("stepTwoOne", pk, sk)
        elif action == 'next' and identify_problems == '':
                return redirect("stepTwoOne", pk, sk)
        elif action == "back":
            return redirect("flowchart", pk, sk)
    if step1: context = {"pk": pk, "sk": sk, "step1": step1}
    else: context = {"pk": pk, "sk": sk}
    return render(request, "stepOne.html", context)


def stepTwoOne(request, pk, sk):
    persons = Person.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name")
        age = request.POST.get("age")
        comment = request.POST.get("comment")
        if action in ('next', 'add') and name!='':
            new_person = Person.objects.create(userId=pk, teamId=sk)
            new_person.name=name
            new_person.age=age
            new_person.comment=comment
            new_person.save()
            if action == 'add':
                return HttpResponseRedirect(request.path_info) 
            elif action == "next":
                return redirect("stepTwoTwo", pk, sk)
        elif action == 'next' and name == '':
                return redirect("stepTwoTwo", pk, sk)
        elif action == "back":
            return redirect("stepOne", pk, sk)
    if persons: context = {"pk": pk, "sk": sk, "persons": persons}
    else: context = {"pk": pk, "sk": sk}
    return render(request, "stepTwoOne.html", context)


def stepTwoTwo(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            selected_problem = request.POST.get("selected_problem")
            step2.selected_problem = selected_problem
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepTwoThree", pk, sk)
        elif action == "back":
            return redirect("stepTwoOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoTwo.html", context)


def stepTwoThree(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            define_problem = request.POST.get("define_problem")
            step2.define_problem = define_problem
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepTwoFour", pk, sk)
        elif action == "back":
            return redirect("stepTwoTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoThree.html", context)


def stepTwoFour(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            desired_solution = request.POST.get("desired_solution")
            step2.desired_solution = desired_solution
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeOne", pk, sk)
        elif action == "back":
            return redirect("stepTwoThree", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoFour.html", context)


def stepThreeOne(request, pk, sk):
    researches = Research.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        research = request.POST.get("research")
        if action in ('next', 'add') and research!='':
            new_research=Research.objects.create(userId=pk, teamId=sk)
            new_research.research=research
            new_research.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeTwo", pk, sk)
        elif action == 'next' and research == '':
                return redirect("stepThreeTwo", pk, sk)
        elif action == "back":
            return redirect("stepTwoFour", pk, sk)
    if researches: context = {"pk": pk, "sk": sk, "researches": researches}
    else: context = {"pk": pk, "sk": sk}
    return render(request, "stepThreeOne.html", context)


def stepThreeTwo(request, pk, sk):
    step3 = StepThree.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            sources = request.POST.get("sources")
            step3.sources = sources
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeThree", pk, sk)
        elif action == "back":
            return redirect("stepThreeOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step3": step3}
    return render(request, "stepThreeTwo.html", context)


def stepThreeThree(request, pk, sk):
    step3 = StepThree.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            difference = request.POST.get("difference")
            step3.difference = difference
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFourOne", pk, sk)
        elif action == "back":
            return redirect("stepThreeTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step3": step3}
    return render(request, "stepThreeThree.html", context)


def stepFourOne(request, pk, sk):
    step4 = StepFour.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step4:
        step4 = StepFour.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            details = request.POST.get("details")
            step4.details = details
            step4.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFourTwo", pk, sk)
        elif action == "back":
            return redirect("stepThreeThree", pk, sk)
    context = {"pk": pk, "sk": sk, "step4": step4}
    return render(request, "stepFourOne.html", context)


def stepFourTwo(request, pk, sk):
    step4 = StepFour.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            difference = request.POST.get("difference")
            step4.difference = difference
            step4.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFiveOne", pk, sk)
        elif action == "back":
            return redirect("stepFourOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step4": step4}
    return render(request, "stepFourTwo.html", context)


def stepFiveOne(request, pk, sk):
    step5 = StepFive.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step5:
        step5 = StepFive.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            talk_to_expert = request.POST.get("talk_to_expert")
            step5.talk_to_expert = talk_to_expert
            step5.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFiveTwo", pk, sk)
        elif action == "back":
            return redirect("stepFourTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step5": step5}
    return render(request, "stepFiveOne.html", context)


def stepFiveTwo(request, pk, sk):
    step5 = StepFive.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            other_information = request.POST.get("other_information")
            step5.other_information = other_information
            step5.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepSix", pk, sk)
        elif action == "back":
            return redirect("stepFiveOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step5": step5}
    return render(request, "stepFiveTwo.html", context)


def stepSix(request, pk, sk):
    if request.method == "POST":
        prototype = request.FILES.get("prototype")
        image_data = prototype.read()
        my_model = StepSix(prototype=image_data)
        my_model.save()
    return render(request, "stepSix.html")


def stepSeven(request, pk, sk):
    step7 = StepSeven.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step7:
        step7 = StepFive.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            testing = request.POST.get("testing")
            step7.testing = testing
            step7.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("guidelines", pk, sk)
        elif action == "back":
            return redirect("stepSix", pk, sk)
    context = {"pk": pk, "sk": sk, "step7": step7}
    return render(request, "stepSeven.html", context)


def guidelines(request, pk, sk):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "save":
            return HttpResponseRedirect(request.path_info)
        elif action == "next":
            return redirect("stepEightOne", pk, sk)
        elif action == "back":
            return redirect("stepSeven", pk, sk)
    context = {"pk": pk, "sk": sk}
    return render(request, "guidelines.html", context)


def stepEightOne(request, pk, sk):
    step8 = StepEight.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step8:
        step8 = StepEight.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            naming = request.POST.get("naming")
            step8.naming = naming
            step8.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepEightTwo", pk, sk)
        elif action == "back":
            return redirect("guidelines", pk, sk)
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightOne.html", context)


def stepEightTwo(request, pk, sk):
    step8 = StepEight.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            where_to_buy = request.POST.get("where_to_buy")
            step8.where_to_buy = where_to_buy
            step8.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepEightThree", pk, sk)
        elif action == "back":
            return redirect("stepEightOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightTwo.html", context)


def stepEightThree(request, pk, sk):
    step8 = StepEight.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            where_to_buy = request.POST.get("where_to_buy")
            step8.where_to_buy = where_to_buy
            step8.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("notes", pk, sk)
        elif action == "back":
            return redirect("stepEightTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightThree.html", context)
