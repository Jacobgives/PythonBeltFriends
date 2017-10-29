from django.db import models
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_user_r(self,post_data):
        response_to_views ={}
        TheUser=User.objects.filter(email=post_data['email'])
        if TheUser:
            response_to_views['status']=False
            response_to_views['errors']={'user':"Username alredy exists"}
            return response_to_views
        errors={}
        name_Match=re.compile(r'^[a-zA-Z ]{3,255}$')
        input_valid=True
        if not re.match(name_Match, post_data['name']) or not re.match(name_Match, post_data['alias']):
            input_valid=False
            errors["alias"] = "name and alias should be more than 2 characters."
        if len(post_data['p'])<8 or post_data['p']!= post_data['cp']:
            input_valid=False
            errors['pass'] = "Password must be at least 8 characters and must match."
        response_to_views['errors']=errors
        if input_valid:
            print('got here')
            new_user = self.create(
            name=post_data['name'],
            alias=post_data['alias'],
            email=post_data['email'],
            password=bcrypt.hashpw(post_data['p'].encode(), bcrypt.gensalt())
            )
            response_to_views['status']=True
            response_to_views['id']=new_user.id
            return response_to_views
        response_to_views['status']=False
        return response_to_views
    def validate_user_l(self, post_data):
        response_to_views={}
        TheUser=self.filter(email=post_data['lemail'])
        errors={}
        if TheUser:
            if bcrypt.checkpw(post_data['lp'].encode(), TheUser[0].password.encode()):
                response_to_views['status']=True
                response_to_views['id']=TheUser[0].id
                return response_to_views
            errors['password']="Invalud password for user."
        errors['user']="User does not exist."
        response_to_views['errors']=errors
        response_to_views['status']=False
        return response_to_views

class User(models.Model):
    alias = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email= models.EmailField(max_length=255, unique=True)
    password= models.CharField(max_length=255)
    mapping=models.ManyToManyField('self', related_name='friends')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
