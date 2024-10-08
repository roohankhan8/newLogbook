from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connections
from django.contrib import messages

from django.urls import reverse
from email.utils import parsedate
from website.utils import has_data_changed

from .forms import *
from .models import *

# Create your views here.

pages = {
    "1": "statementOfOriginality",
    "2": "stepOne",
    "3": "stepTwoOne",
    "4": "stepThreeOne",
    "5": "stepFourTwo",
    "6": "stepSix",
    "7": "stepEightThree",
}
models = {
    "1": StatementOfOriginality,
    "2": StepOne,
    "3": Person,
    "4": Research,
    "5": Issue,
    "6": StepSix,
    "7": Customer,
}


def calling_functions(func_id, request, pk, sk):
    func_id = int(func_id)
    if func_id == 1:
        statementOfOriginality(request, pk, sk)
    elif func_id == 2:
        stepOne(request, pk, sk)
    elif func_id == 3:
        stepTwoOne(request, pk, sk)
    elif func_id == 4:
        stepThreeOne(request, pk, sk)
    elif func_id == 5:
        stepFourTwo(request, pk, sk)
    elif func_id == 6:
        stepSix(request, pk, sk)
    elif func_id == 7:
        stepEightThree(request, pk, sk)


# pk -> page/model, sk -> recordId, tk -> teamId, fk -> userId
def deleteInfo(request, pk, sk, tk, fk):
    record = get_object_or_404(models[pk], id=sk)
    record.delete()
    # messages.success(request, "The statement has been deleted successfully.")
    return redirect(pages[pk], tk, fk)


# pk -> teamId, sk -> userId, tk -> page/model, fk -> recordId
def showInfo(request, pk, sk, tk, fk, args):
    record = get_object_or_404(models[tk], id=int(fk))
    if args == "1":
        data = StepOne.objects.filter(teamId=sk).order_by("-date_updated")
    else:
        data=None
    all_records = models[tk].objects.filter(teamId=sk).order_by("-date_updated")
    context = {
        "pk": pk,
        "sk": sk,
        "all_records": all_records,
        "record": record,
        "data": data,
    }
    if request.method == "POST":
        calling_functions(tk, request, pk, sk)
        record.delete()
        return redirect(pages[tk], pk=pk, sk=sk)
    if record:
        return render(request, f"{pages[tk]}.html", context)


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


# def teams(request, pk):
#     student_id = pk
#     with connections["user_database"].cursor() as cursor:
#         # Get all team IDs associated with the student in one query
#         cursor.execute(
#             """
#             SELECT tm.team_id, t.name
#             FROM tbl_team_member tm
#             JOIN tbl_team t ON tm.team_id = t.id
#             WHERE tm.student_id = %s
#             """, [student_id]
#         )
#         teams_data = cursor.fetchall()
#     # Create a dictionary with team_id as key and team name as value
#     teams = {team_id: team_name for team_id, team_name in teams_data}
#     context = {"pk": pk, "teams": teams}
#     return render(request, "teams.html", context)


def teams(request, pk):
    student_id = pk
    with connections["user_database"].cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tbl_team_member WHERE student_id=%s", [student_id]
        )
        user_data = cursor.fetchall()
    teams = {}
    team_ids = []
    all_teams = []
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
    with connections["user_database"].cursor() as cursor:
        cursor.execute("SELECT * FROM tbl_team WHERE id=%s", [team_id])
        team_data = cursor.fetchone()
    context = {"pk": pk, "sk": sk, "user": user_data, "team": team_data}
    return render(request, "outline.html", context)


def flowchart(request, pk, sk):
    context = {"pk": pk, "sk": sk}
    return render(request, "flowchart.html", context)


def recordOfInvention(request, pk, sk):
    record, created = RecordOfInvention.objects.get_or_create(
        teamId=sk,
        defaults={"userId": pk},
    )
    if request.method == "POST":
        record.name_of_invention = request.POST.get(
            "name_of_invention", record.name_of_invention
        )
        record.problem_it_solves = request.POST.get(
            "problem_it_solves", record.problem_it_solves
        )
        record.save()
        return redirect("statementOfOriginality", pk, sk)
    context = {"pk": pk, "sk": sk, "record": record}
    return render(request, "recordOfInvention.html", context)


def statementOfOriginality(request, pk, sk):
    all_records = StatementOfOriginality.objects.filter(teamId=sk).order_by(
        "-date_updated"
    )
    # if int(tk) >= 0:
    #     record = get_object_or_404(models[tk], id=fk)
    #     context = {"pk": pk, "sk": sk, "statement": statement, "record": record}
    #     if record:
    #         record.delete()
    #         return render(request, "statementOfOriginality.html", context)
    if request.method == "POST":
        action = request.POST.get("action")
        inventor = request.POST.get("inventor")
        schoolnamegrade = request.POST.get("schoolnamegrade")
        sign = request.POST.get("sign")
        if action in ("add", "next") and inventor:
            new_statement = StatementOfOriginality.objects.create(userId=pk, teamId=sk)
            new_statement.inventor = inventor
            new_statement.schoolnamegrade = schoolnamegrade
            new_statement.sign = sign
            new_statement.save()
            if action == "add":
                return redirect("statementOfOriginality", pk=pk, sk=sk)
            return redirect("flowchart", pk=pk, sk=sk)
        elif action == "next" and not inventor:
            return redirect("flowchart", pk=pk, sk=sk)
        elif action == "back":
            return redirect("recordOfInvention", pk, sk)
    context = {"pk": pk, "sk": sk, "all_records": all_records}
    return render(request, "statementOfOriginality.html", context)


def stepOne(request, pk, sk):
    step1 = StepOne.objects.filter(teamId=sk).order_by("-date_updated")
    if request.method == "POST":
        action = request.POST.get("action")
        identify_problems = request.POST.get("identify_problems")
        problems = request.POST.get("problems")
        if action in ("next", "add") and identify_problems:
            StepOne.objects.create(
                userId=pk,
                teamId=sk,
                identify_problems=identify_problems,
                problems=problems,
            )
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepTwoOne", pk, sk)
        if action == "next" and not identify_problems:
            return redirect("stepTwoOne", pk, sk)
        if action == "back":
            return redirect("flowchart", pk, sk)
    context = {"pk": pk, "sk": sk, "all_records": step1}
    return render(request, "stepOne.html", context)


def stepTwoOne(request, pk, sk):
    step1 = StepOne.objects.filter(teamId=sk).order_by("-date_updated")
    persons = Person.objects.filter(teamId=sk).order_by("-date_updated")
    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name")
        if action in ("next", "add") and name != "":
            Person.objects.create(
                userId=pk,
                teamId=sk,
                problem=request.POST.get("problem", ""),
                name=name,
                age=request.POST.get("age", 0),
                comment=request.POST.get("comment", ""),
            )
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepTwoTwo", pk, sk)
        if action == "next" and not name:
            return redirect("stepTwoTwo", pk, sk)
        if action == "back":
            return redirect("stepOne", pk, sk)
    context = {"pk": pk, "sk": sk, "data": step1, "all_records": persons}
    return render(request, "stepTwoOne.html", context)


def stepTwoTwo(request, pk, sk):
    step2, created = StepTwo.objects.get_or_create(teamId=sk, defaults={"userId": pk})
    if request.method == "POST":
        action = request.POST.get("action")
        selected_problem = request.POST.get("selected_problem", "")
        if action in ("save", "next") and selected_problem:
            step2.selected_problem = selected_problem
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepTwoThree", pk, sk)
        if action == "next" and not selected_problem:
            return redirect("stepTwoThree", pk, sk)
        if action == "back":
            return redirect("stepTwoOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoTwo.html", context)


def stepTwoThree(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        define_problem = request.POST.get("define_problem", "")
        if action in ("save", "next") and define_problem:
            step2.define_problem = define_problem
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepTwoFour", pk, sk)
        if action == "next" and not define_problem:
            return redirect("stepTwoFour", pk, sk)
        if action == "back":
            return redirect("stepTwoTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoThree.html", context)


def stepTwoFour(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        desired_solution = request.POST.get("desired_solution", "")
        if action in ("save", "next") and desired_solution:
            step2.desired_solution = desired_solution
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepThreeOne", pk, sk)
        if action == "next" and not desired_solution:
            return redirect("stepThreeOne", pk, sk)
        if action == "back":
            return redirect("stepTwoThree", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoFour.html", context)


def stepThreeOne(request, pk, sk):
    researches = Research.objects.filter(teamId=sk).order_by("-date_updated")
    if request.method == "POST":
        action = request.POST.get("action")
        research = request.POST.get("research", "")
        if action in ("next", "add") and research:
            Research.objects.create(userId=pk, teamId=sk, research=research)
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepThreeTwo", pk, sk)
        if action == "next" and not research:
            return redirect("stepThreeTwo", pk, sk)
        if action == "back":
            return redirect("stepTwoFour", pk, sk)
    context = {"pk": pk, "sk": sk, "all_records": researches}
    return render(request, "stepThreeOne.html", context)


def stepThreeTwo(request, pk, sk):
    step3, created = StepThree.objects.get_or_create(teamId=sk, defaults={"userId": pk})
    if request.method == "POST":
        action = request.POST.get("action")
        sources = request.POST.get("sources", "")
        if action in ("save", "next") and sources:
            step3.sources = sources
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepThreeThree", pk, sk)
        elif action == "next" and not sources:
            return redirect("stepThreeThree", pk, sk)
        elif action == "back":
            return redirect("stepThreeOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step3": step3}
    return render(request, "stepThreeTwo.html", context)


def stepThreeThree(request, pk, sk):
    step3 = StepThree.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        difference = request.POST.get("difference", "")
        if action in ("save", "next") and difference:
            step3.difference = difference
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepFourOne", pk, sk)
        elif action == "next" and not difference:
            return redirect("stepFourOne", pk, sk)
        elif action == "back":
            return redirect("stepThreeTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step3": step3}
    return render(request, "stepThreeThree.html", context)


def stepFourOne(request, pk, sk):
    step4, created = StepFour.objects.get_or_create(teamId=sk, defaults={"userId": pk})
    if request.method == "POST":
        action = request.POST.get("action")
        details = request.POST.get("details", "")
        if action in ("save", "next") and details:
            step4.details = details
            step4.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepFourTwo", pk, sk)
        if action == "next" and not details:
            return redirect("stepFourTwo", pk, sk)
        if action == "back":
            return redirect("stepThreeThree", pk, sk)
    context = {"pk": pk, "sk": sk, "step4": step4}
    return render(request, "stepFourOne.html", context)


def stepFourTwo(request, pk, sk):
    issues = Issue.objects.filter(teamId=sk).order_by("-date_updated")
    if request.method == "POST":
        action = request.POST.get("action")
        expert_name = request.POST.get("expert_name")
        expert_credentials = request.POST.get("expert_credentials")
        problem_identified = request.POST.get("problem_identified")
        problem_faced = request.POST.get("problem_faced")
        if action in ("next", "add") and expert_name:
            Issue.objects.create(
                userId=pk,
                teamId=sk,
                expert_name=expert_name,
                expert_credentials=expert_credentials,
                problem_identified=problem_identified,
                problem_faced=problem_faced,
            )
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepFiveOne", pk, sk)
        if action == "next" and expert_name == "":
            return redirect("stepFiveOne", pk, sk)
        if action == "back":
            return redirect("stepFourOne", pk, sk)
    context = {"pk": pk, "sk": sk, "all_records": issues}
    return render(request, "stepFourTwo.html", context)


def stepFiveOne(request, pk, sk):
    step5, created = StepFive.objects.get_or_create(teamId=sk, defaults={"userId": pk})
    if request.method == "POST":
        action = request.POST.get("action")
        talk_to_expert = request.POST.get("talk_to_expert", "")
        if action in ("save", "next"):
            step5.talk_to_expert = talk_to_expert
            step5.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepFiveTwo", pk, sk)
        if action == "back":
            return redirect("stepFourTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step5": step5}
    return render(request, "stepFiveOne.html", context)


def stepFiveTwo(request, pk, sk):
    step5 = StepFive.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        other_information = request.POST.get("other_information", "")
        if action in ("save", "next"):
            step5.other_information = other_information
            step5.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepSix", pk, sk)
        if action == "back":
            return redirect("stepFiveOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step5": step5}
    return render(request, "stepFiveTwo.html", context)


def viewImage(request, pk):
    image = StepSix.objects.get(id=pk)
    return HttpResponse(image.prototype, content_type="image/jpeg")


def stepSix(request, pk, sk):
    step6 = StepSix.objects.filter(teamId=sk).order_by("-date_updated")
    if request.method == "POST":
        action = request.POST.get("action")
        arrange_material = request.POST.get("arrange_material")
        prototype = request.FILES.get("prototype")
        if action in ("next", "add") and arrange_material and prototype:
            image_data = prototype.read()
            new_prototype = StepSix.objects.create(userId=pk, teamId=sk)
            new_prototype.arrange_material = arrange_material
            new_prototype.prototype = image_data
            new_prototype.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepSeven", pk, sk)
        if action == "next" and not arrange_material:
            return redirect("stepSeven", pk, sk)
        if action == "back":
            return redirect("stepFiveTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "all_records": step6}
    return render(request, "stepSix.html", context)


def stepSeven(request, pk, sk):
    step7, created = StepSeven.objects.get_or_create(teamId=sk, defaults={"userId": pk})
    if request.method == "POST":
        action = request.POST.get("action")
        testing = request.POST.get("testing", "")
        if action in ("save", "next") and testing:
            step7.testing = testing
            step7.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("guidelines", pk, sk)
        if action == "next" and not testing:
            return redirect("guidelines", pk, sk)
        if action == "back":
            return redirect("stepSix", pk, sk)
    context = {"pk": pk, "sk": sk, "step7": step7}
    return render(request, "stepSeven.html", context)


def guidelines(request, pk, sk):
    context = {"pk": pk, "sk": sk}
    return render(request, "guidelines.html", context)


def stepEightOne(request, pk, sk):
    step8, created = StepEight.objects.get_or_create(teamId=sk, defaults={"userId": pk})
    if request.method == "POST":
        action = request.POST.get("action")
        naming = request.POST.get("naming")
        if action in ("save", "next") and naming:
            step8.naming = naming
            step8.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            return redirect("stepEightTwo", pk, sk)
        if action == "back":
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
            return redirect("stepEightThree", pk, sk)
        if action == "back":
            return redirect("stepEightOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step8": step8}
    return render(request, "stepEightTwo.html", context)


def stepEightThree(request, pk, sk):
    customers = Customer.objects.filter(teamId=sk).order_by("-date_updated")
    if request.method == "POST":
        action = request.POST.get("action")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        education = request.POST.get("education")
        household = request.POST.get("household")
        marital_status = request.POST.get("marital_status")
        if action in ("next", "add") and age:
            Customer.objects.create(
                userId=pk,
                teamId=sk,
                age=age,
                gender=gender,
                education=education,
                household=household,
                marital_status=marital_status,
            )
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            return redirect("courseOutline", pk, sk)
        if action == "next" and not age:
            return redirect("courseOutline", pk, sk)
        if action == "back":
            return redirect("stepEightTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "all_records": customers}
    return render(request, "stepEightThree.html", context)


def notes(request, pk, sk):
    context = {"pk": pk, "sk": sk}
    return render(request, "notes.html", context)


def previewLogbook(request, pk, sk):
    return render(request, "previewLogbook.html")


def survey(request, pk, sk):
    return render(request, "survey.html")
