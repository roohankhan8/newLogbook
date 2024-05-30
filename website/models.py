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

class Inventor(models.Model):
    inventor = models.TextField()
    schoolnamegrade = models.TextField()
    sig = models.TextField()
    date = models.TextField()

class StatementOfOriginality(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    inventors=models.ManyToManyField(Inventor, related_name='statement_of_originality')

    def __str__(self):
        return str(self.teamId)

class StepOne(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)

    identify_problems = models.TextField()

    def __str__(self):
        return str(self.teamId)

class Problem(models.Model):
    problem=models.TextField()
    name1=models.TextField()
    name2=models.TextField()
    name3=models.TextField()
    name4=models.TextField()
    age1=models.TextField()
    age2=models.TextField()
    age3=models.TextField()
    age4=models.TextField()
    comment1=models.TextField()
    comment2=models.TextField()
    comment3=models.TextField()
    comment4=models.TextField()


class StepTwo(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    problems=models.ManyToManyField(Problem, related_name='step_two')
    #2.1
    problem_title = models.TextField()
    problem_description = models.TextField()
    #2.2
    selected_problem=models.TextField(null=True, blank=True)
    #2.2.1
    define_problem=models.TextField(null=True, blank=True)
    #2.3
    desired_solution=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)

class StepThree(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    research=models.TextField(null=True, blank=True)
    sources=models.TextField(null=True, blank=True)
    difference=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)

class StepFour(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    details=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)
    
class StepFive(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    talk_to_expert=models.TextField(null=True, blank=True)
    other_information=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)

class StepSix(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    arrange_material=models.TextField(null=True, blank=True)
    prototype=models.BinaryField(blank=True) 
    
    def __str__(self):
        return str(self.teamId)

class StepSeven(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    testing=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)

class StepEight(models.Model):
    userId = models.IntegerField()
    teamId = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    
    naming=models.TextField(null=True, blank=True)
    where_to_buy=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.teamId)
