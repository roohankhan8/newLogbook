from django.db import models

# Create your models here.


class RecordOfInvention(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    name_of_invention = models.CharField(max_length=30, blank=True)
    problem_it_solves = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.teamId)

class StatementOfOriginality(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    inventor=models.CharField(max_length=255, null=True, blank=True)
    schoolnamegrade=models.CharField(max_length=255, null=True, blank=True)
    date=models.DateField(max_length=255, null=True, blank=True)
    sign=models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class StepOne(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    identify_problems = models.CharField(max_length=255)
    problems = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class Person(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    problem = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True, null=True, default=1)
    comment = models.CharField(max_length=30)

    def __str__(self):
        return str(self.teamId)


class StepTwo(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    # 2.2
    selected_problem = models.TextField(null=True, blank=True)
    # 2.2.1
    define_problem = models.TextField(null=True, blank=True)
    # 2.3
    desired_solution = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class Research(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    research = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class StepThree(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    sources = models.TextField(null=True, blank=True)
    difference = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class Issue(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    expert_name = models.TextField(null=True, blank=True)
    expert_credentials = models.TextField(null=True, blank=True)
    problem_identified = models.TextField(null=True, blank=True)
    problem_faced = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class StepFour(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class StepFive(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    talk_to_expert = models.TextField(null=True, blank=True)
    other_information = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)


class StepSix(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    arrange_material = models.TextField(null=True, blank=True)
    prototype = models.BinaryField(blank=True)

    def __str__(self):
        return str(self.teamId)


class StepSeven(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    testing = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)

class Customer(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    age=models.IntegerField(null=True, blank=True)
    gender=models.CharField(max_length=255, null=True, blank=True)
    education=models.CharField(max_length=255, null=True, blank=True)
    household=models.CharField(max_length=255, null=True, blank=True)
    marital_status=models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)
class StepEight(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    naming = models.TextField(null=True, blank=True)
    where_to_buy = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.teamId)
