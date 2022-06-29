import imp
from posixpath import split
from re import U
from turtle import update
from django.db import models
import re
from datetime import *



# Create your models here.
class loginManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fName']) <2:
            errors['fName'] ="first name should be at least 2 characters long"
        if len(postData['lName']) <2:
            errors['lName'] ="last name should be at least 2 characters long"
        if not EMAIL_REGEX.match(postData['Email']):
            errors["Email"] = "invalid email address"
        if  postData['password'] != postData['confirm']:
            errors["Confirm"] = "confirm password should be same as password"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors   

class tripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        now = datetime.now()
        
        
        

        if len(postData['dest'])==0:
            errors['dest'] = "destination must be provided"
        if len(postData['dest'])<3:
            errors['dest'] = "destination must be at least 3 characters long"
        if len(postData['plan'])== 0:
            errors['plan'] = 'plan must be provided'
        if len(postData['plan'])<3:
            errors['plan']= "plan must be 3 characters long"
        if len(postData['SDate'] ) == 0:
            errors['SDate'] = "please chose a starting date"
        else:
            SDate =  datetime.strptime(postData['SDate'],"%Y-%m-%d")
        if len(postData['EDate'] ) == 0:
            errors['EDate'] = "please choose an ending date"
        else:
            EDate = datetime.strptime(postData['EDate'],"%Y-%m-%d")
            if SDate>EDate :
                errors["EDate"] = "time traveling isn't allowed cant end before you start!"
            if SDate<now:
                errors["SDate"] = "time travel isn't allowed!! how can you start in the past??!"
        
        
        return errors
class User(models.Model):
    fName = models.CharField(max_length=255)
    lName = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = loginManager()


class trips(models.Model):
    dest = models.CharField(max_length=255)
    SDate = models.DateField()
    EDate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=255)
    user = models.ForeignKey(User,related_name="trip",on_delete=models.CASCADE)
    memebers = models.ManyToManyField(User, related_name="trips")
    objects = tripManager()