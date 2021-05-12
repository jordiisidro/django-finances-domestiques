from django.db import models


from django_userforeignkey.models.fields import UserForeignKey


class ClasseBase(models.Model):
    estat = models.BooleanField(default=True)
    dataCreacio = models.DateTimeField(auto_now_add=True)
    dataModificacio = models.DateTimeField(auto_now=True)
    usuariCreacio = UserForeignKey(auto_user_add=True,related_name='+')
    usuariModificacio = UserForeignKey(auto_user=True,related_name='+')

    class Meta:
        abstract=True
        
        

