from email.utils import parsedate
from django.db import connections
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse

from website.utils import has_data_changed
from .forms import *
from .models import *

# Create your views here.

pages = {
    '1': 'statementOfOriginality',
    '2': 'stepOne',
    '3': 'stepTwoOne',
    '4': 'stepThreeOne',
    '5': 'stepFourTwo',
    '6': 'stepSix',
    '7': 'stepEightThree',
}


def deleteInfo(request, pk, sk, tk, fk):
    if pk == "1": record = get_object_or_404(StatementOfOriginality, id=sk)
    if pk == "2": record = get_object_or_404(StepOne, id=sk)
    if pk == "3": record = get_object_or_404(Person, id=sk)
    if pk == "4": record = get_object_or_404(Research, id=sk)
    if pk == "5": record = get_object_or_404(Issue, id=sk)
    if pk == "6": record = get_object_or_404(StepSix, id=sk)
    if pk == "7": record = get_object_or_404(Customer, id=sk)
    record.delete()
    messages.success(request, "The statement has been deleted successfully.")
    return redirect(pages[pk], tk, fk)

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
    if not record:
        record = RecordOfInvention.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        name_of_invention = request.POST.get("name_of_invention")
        problem_it_solves = request.POST.get("problem_it_solves")
        record.name_of_invention = name_of_invention
        record.problem_it_solves = problem_it_solves
        record.save()
        return redirect("statementOfOriginality", pk, sk)
    if record:
        context = {"pk": pk, "sk": sk, "record": record}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "recordOfInvention.html", context)


def statementOfOriginality(request, pk, sk):
    statement = (
        StatementOfOriginality.objects.filter(teamId=sk).order_by("-date_updated").all()
    )
    if request.method == "POST":
        action = request.POST.get("action")
        inventor = request.POST.get("inventor")
        schoolnamegrade = request.POST.get("schoolnamegrade")
        sign = request.POST.get("sign")
        date = parsedate(request.POST.get("date"))
        if action in ("add", "next") and inventor:
            new_statement = StatementOfOriginality.objects.create(userId=pk, teamId=sk)
            new_statement.inventor = inventor
            new_statement.schoolnamegrade = schoolnamegrade
            new_statement.sign = sign
            new_statement.date = date
            new_statement.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("flowchart", pk=pk, sk=sk)
        elif action == "next" and not inventor:
            return redirect("flowchart", pk=pk, sk=sk)
        elif action == "back":
            return redirect("recordOfInvention", pk, sk)
    context = {"pk": pk, "sk": sk, "statement": statement}
    return render(request, "statementOfOriginality.html", context)


def stepOne(request, pk, sk):
    step1 = StepOne.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        identify_problems = request.POST.get("identify_problems")
        if action in ("next", "add") and identify_problems != "":
            new_problem = StepOne.objects.create(userId=pk, teamId=sk)
            new_problem.identify_problems = identify_problems
            new_problem.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepTwoOne", pk, sk)
        elif action == "next" and identify_problems == "":
            return redirect("stepTwoOne", pk, sk)
        elif action == "back":
            return redirect("flowchart", pk, sk)
    if step1:
        context = {"pk": pk, "sk": sk, "step1": step1}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "stepOne.html", context)


def stepTwoOne(request, pk, sk):
    persons = Person.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name")
        age = request.POST.get("age")
        comment = request.POST.get("comment")
        if action in ("next", "add") and name != "":
            new_person = Person.objects.create(userId=pk, teamId=sk)
            new_person.name = name
            new_person.age = age
            new_person.comment = comment
            new_person.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepTwoTwo", pk, sk)
        elif action == "next" and name == "":
            return redirect("stepTwoTwo", pk, sk)
        elif action == "back":
            return redirect("stepOne", pk, sk)
    if persons:
        context = {"pk": pk, "sk": sk, "persons": persons}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "stepTwoOne.html", context)


def stepTwoTwo(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step2:
        step2 = StepTwo.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        selected_problem = request.POST.get("selected_problem")
        if action in ("save", "next") and selected_problem != "":
            step2.selected_problem = selected_problem
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepTwoThree", pk, sk)
        elif action == "next" and selected_problem == "":
            return redirect("stepTwoThree", pk, sk)
        elif action == "back":
            return redirect("stepTwoOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoTwo.html", context)


def stepTwoThree(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        define_problem = request.POST.get("define_problem")
        if action in ("save", "next") and define_problem != "":
            step2.define_problem = define_problem
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepTwoFour", pk, sk)
        elif action == "next" and define_problem == "":
            return redirect("stepTwoFour", pk, sk)
        elif action == "back":
            return redirect("stepTwoTwo", pk, sk)
    context = {"pk": pk, "sk": sk, "step2": step2}
    return render(request, "stepTwoThree.html", context)


def stepTwoFour(request, pk, sk):
    step2 = StepTwo.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        desired_solution = request.POST.get("desired_solution")
        if action in ("save", "next") and desired_solution != "":
            step2.desired_solution = desired_solution
            step2.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeOne", pk, sk)
        elif action == "next" and desired_solution == "":
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
        if action in ("next", "add") and research != "":
            new_research = Research.objects.create(userId=pk, teamId=sk)
            new_research.research = research
            new_research.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeTwo", pk, sk)
        elif action == "next" and research == "":
            return redirect("stepThreeTwo", pk, sk)
        elif action == "back":
            return redirect("stepTwoFour", pk, sk)
    if researches:
        context = {"pk": pk, "sk": sk, "researches": researches}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "stepThreeOne.html", context)


def stepThreeTwo(request, pk, sk):
    step3 = StepThree.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step3:
        step3 = StepThree.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        sources = request.POST.get("sources")
        if action in ("save", "next") and sources != "":
            step3.sources = sources
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepThreeThree", pk, sk)
        elif action == "next" and sources == "":
            return redirect("stepThreeThree", pk, sk)
        elif action == "back":
            return redirect("stepThreeOne", pk, sk)
    context = {"pk": pk, "sk": sk, "step3": step3}
    return render(request, "stepThreeTwo.html", context)


def stepThreeThree(request, pk, sk):
    step3 = StepThree.objects.filter(teamId=sk).order_by("-date_updated").first()
    if request.method == "POST":
        action = request.POST.get("action")
        difference = request.POST.get("difference")
        if action in ("save", "next") and difference != "":
            step3.difference = difference
            step3.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFourOne", pk, sk)
        elif action == "next" and difference == "":
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
        details = request.POST.get("details")
        if action in ("save", "next") and details != "":
            step4.details = details
            step4.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFourTwo", pk, sk)
        elif action == "next" and details == "":
            return redirect("stepFourTwo", pk, sk)
        elif action == "back":
            return redirect("stepThreeThree", pk, sk)
    if step4:
        context = {"pk": pk, "sk": sk, "step4": step4}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "stepFourOne.html", context)


def stepFourTwo(request, pk, sk):
    issues = Issue.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        expert_name = request.POST.get("expert_name")
        expert_credentials = request.POST.get("expert_credentials")
        problem_identified = request.POST.get("problem_identified")
        problem_faced = request.POST.get("problem_faced")
        if action in ("next", "add") and expert_name != "":
            new_issue = Issue.objects.create(userId=pk, teamId=sk)
            new_issue.expert_name = expert_name
            new_issue.expert_credentials = expert_credentials
            new_issue.problem_identified = problem_identified
            new_issue.problem_faced = problem_faced
            new_issue.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("stepFiveOne", pk, sk)
        elif action == "next" and expert_name == "":
            return redirect("stepFiveOne", pk, sk)
        elif action == "back":
            return redirect("stepFourOne", pk, sk)
    if issues:
        context = {"pk": pk, "sk": sk, "issues": issues}
    else:
        context = {"pk": pk, "sk": sk}
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


def viewImage(request, pk):
    image = StepSix.objects.get(id=pk)
    return HttpResponse(image.prototype, content_type="image/jpeg")


def stepSix(request, pk, sk):
    step6 = StepSix.objects.filter(teamId=sk).order_by("-date_updated").all()
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
            elif action == "next":
                return redirect("stepSeven", pk, sk)
        elif action == "next" and arrange_material == "":
            return redirect("stepSeven", pk, sk)
        elif action == "back":
            return redirect("stepFiveTwo", pk, sk)
    if step6:
        context = {"pk": pk, "sk": sk, "step6": step6}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "stepSix.html", context)


def stepSeven(request, pk, sk):
    step7 = StepSeven.objects.filter(teamId=sk).order_by("-date_updated").first()
    if not step7:
        step7 = StepSeven.objects.create(userId=pk, teamId=sk)
    if request.method == "POST":
        action = request.POST.get("action")
        testing = request.POST.get("testing")
        if action in ("save", "next") and testing:
            step7.testing = testing
            step7.save()
            if action == "save":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("guidelines", pk, sk)
        elif action == "next" and not testing:
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
    customers = Customer.objects.filter(teamId=sk).order_by("-date_updated").all()
    if request.method == "POST":
        action = request.POST.get("action")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        education = request.POST.get("education")
        household = request.POST.get("household")
        marital_status = request.POST.get("marital_status")
        if action in ("next", "add") and age != "":
            new_customer = Customer.objects.create(userId=pk, teamId=sk)
            new_customer.age = age
            new_customer.gender = gender
            new_customer.education = education
            new_customer.household = household
            new_customer.marital_status = marital_status
            new_customer.save()
            if action == "add":
                return HttpResponseRedirect(request.path_info)
            elif action == "next":
                return redirect("courseOutline", pk, sk)
        elif action == "next" and age == "":
            return redirect("courseOutline", pk, sk)
        elif action == "back":
            return redirect("stepEightTwo", pk, sk)
    if customers:
        context = {"pk": pk, "sk": sk, "customers": customers}
    else:
        context = {"pk": pk, "sk": sk}
    return render(request, "stepEightThree.html", context)


def notes(request, pk, sk):
    context = {"pk": pk, "sk": sk}
    return render(request, "notes.html", context)


def previewLogbook(request, pk, sk):
    return render(request, "previewLogbook.html")


def survey(request, pk, sk):
    return render(request, "survey.html")
