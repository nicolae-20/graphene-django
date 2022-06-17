from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=240)
    name_ro = models.CharField(max_length=240)
    bio = models.CharField(max_length=240)
    bio_ro = models.CharField(max_length=240)
    image = models.ImageField()
    
    def __str__(self):
        return self.name
    
    
class Topic(models.Model):
    name = models.CharField(max_length=240)
    name_ro = models.CharField(max_length=240)
    image = models.ImageField()
    
    def __str__(self):
        return self.name
    
    
class Bootcamp(models.Model):
    name = models.CharField(max_length=240)
    name_ro = models.CharField(max_length=240)
    image = models.ImageField()
    
    def __str__(self):
        return self.name
    
    
class Cohort(models.Model):
    start_date = models.DateField()
    name = models.CharField(max_length=240)
    name_ro = models.CharField(max_length=240)
    bootcamp = models.ForeignKey(
        Bootcamp, related_name="cohorts", on_delete=models.CASCADE
    )
    instructors = models.ManyToManyField(
        Instructor, related_name="cohorts", through="Role"
    )
    
    def __str__(self):
        return self.name
    

class Role(models.Model):
    instructor = models.ForeignKey(
        Instructor, related_name="roles", on_delete=models.CASCADE
    )
    cohort = models.ForeignKey(
        Cohort, related_name="roles", on_delete=models.CASCADE
    )
    topics = models.ManyToManyField(Topic)
    
    def __str__(self):
        return self.cohort.name + " " + str(self.topics)
    
    