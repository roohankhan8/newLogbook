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
    step1 = StepOne.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step1:
        step1 = StepOne.objects.create(userId=pk, teamId=sk)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "save":
            identify_problems = request.POST.get("identify_problems")
           
            step1.problem_title = identify_problems
            step1.save()
            messages.success(request, "Step One data saved successfully.")
            return HttpResponseRedirect(request.path_info)
        elif action == "next":
         
            return redirect("stepTwoOne", pk=pk, sk=sk)
        elif action == "back":
         
            return redirect("flowchart", pk=pk, sk=sk)
        elif action == "add_on":
          
            new_problem = request.POST.get("new_problem")
            if new_problem:
               
                step1.problems.create(description=new_problem)
                messages.success(request, "New problem added successfully.")
            else:
                messages.error(request, "Please enter a problem to add.")
            return HttpResponseRedirect(request.path_info)

    context = {
        "pk": pk,
        "sk": sk,
        "step1": step1,
        "show_add_problem": True,  
    }
    return render(request, "stepOne.html", context)

def stepTwoOne(request, pk, sk):
    step1 = StepOne.objects.filter(teamId=sk).order_by("-date_updated").first()
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()

    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            problem_1 = request.POST.get("problem_1")
            p1name1 = request.POST.get("p1name1")
            p1age1 = request.POST.get("p1age1")
            p1comment1 = request.POST.get("p1comment1")
            problem_title = request.POST.get("problem_title")
            problem_description = request.POST.get("problem_description")
            describe_problem = request.POST.get("describe_problem")
            specific_solution = request.POST.get("specific_solution")
            member1 = Problem.objects.create(
                problem=problem_1,
                name1=p1name1,
                age1=p1age1,
                comment1=p1comment1,
            )

            if step2:
                data_changed = has_data_changed(step2, request.POST)
            else:
                data_changed = True

            if not step2 or data_changed:
                step2 = StepTwo.objects.create(userId=pk, teamId=sk)
                step2.problem_title = problem_title
                step2.problem_description = problem_description
                step2.describe_problem = describe_problem
                step2.specific_solution = specific_solution
                step2.problems.add(member1)
                step2.save()

            if action == "save":
                return redirect("stepTwoOne", pk=pk, sk=sk)
            elif action == "next":
                return redirect("stepTwoTwo", pk=pk, sk=sk)

        elif action == "back":
            return redirect("flowchart", pk=pk, sk=sk)
        elif action == "add_on":
            new_problem = request.POST.get("new_problem")
            if new_problem:
                if not step1:
                    step1 = StepOne.objects.create(userId=pk, teamId=sk)
                step1.problems.create(description=new_problem)
                messages.success(request, "New problem added successfully.")
            else:
                messages.error(request, "Please enter a problem to add.")
            return redirect("stepTwoOne", pk=pk, sk=sk)

    context = {"pk": pk, "sk": sk, "step1": step1, "step2": step2, "show_add_problem": True}
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
    step3 = StepThree.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step3:
        step3 = StepThree.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            research = request.POST.get("research")
            step3.research = research
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeTwo", pk, sk)
        elif action == "back":
            return redirect("stepTwoFour", pk, sk)
    context = {"pk": pk, "sk": sk, "step3": step3}
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
            difference = request.POST.get("difference")
            step4.difference = difference
            step4.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFourTwo", pk, sk)
        elif action == "back":
            return redirect("stepThreeThree", pk, sk)
    context = {"pk": pk, "sk": sk, "step4": step4}
    return render(request, "stepFourTwo.html", context)


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
        step5 = StepFour.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save", "next"):
            difference = request.POST.get("difference")
            step5.difference = difference
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
            difference = request.POST.get("difference")
            step5.difference = difference
            step5.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepSix", pk, sk)
        elif action == "back":
            return redirect("stepFiveOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step5": step5}
    return render(request, "stepFiveTwo.html", context)


def stepSix(request):
    if request.method == "POST":
        prototype = request.FILES.get("prototype")
        image_data = prototype.read()
        my_model = StepSix(prototype=image_data)
        my_model.save()
    return render(request, "stepSix.html")


def stepSeven(request):
    if request.method == "POST":
        prototype = request.FILES.get("prototype")
        image_data = prototype.read()
        my_model = StepSeven(prototype=image_data)
        my_model.save()
    return render(request, "stepSeven.html")


def guidelines(request):
    return render(request, "guidelines.html")


def stepEightOne(request, pk, sk):
    step8 = StepEight.objects.filter(teamId=sk).order_by("-date_updated").first()
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightOne.html", context)


def stepEightTwo(request, pk, sk):
    step8 = StepEight.objects.filter(teamId=sk).order_by("-date_updated").first()
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightTwo.html", context)


def stepEightThree(request, pk, sk):
    step8 = StepEight.objects.filter(teamId=sk).order_by("-date_updated").first()
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightThree.html", context)
