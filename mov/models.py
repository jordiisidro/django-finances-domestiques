from django.db import models

from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User

import re

from bases.models import ClasseBase



def validate_color(value):
    rg = re.compile("#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]")   
    if rg.match(value)==None:
        raise ValidationError("Format de color invalid") 
    else:
        return value

class GrupMoviment(ClasseBase):
    descripcio = models.CharField(
        max_length=100,
        help_text='Descripcio del grup de Moviment',
        unique=True
    )

    color = models.CharField(default='#FF0000', null=True, blank=True, validators =[validate_color] , max_length=7 )
    
    def __str__(self):
        return '{}'.format(self.descripcio)

    def save(self):
        self.descripcio = self.descripcio.upper()
        self.color = self.color.upper()
        super(GrupMoviment, self).save()

    class Meta:
        verbose_name_plural= "Grups de Moviment"
        ordering  = ["descripcio"]
        
class SubgrupMoviment(ClasseBase):
    grupMoviment = models.ForeignKey(GrupMoviment, on_delete=models.PROTECT)
    descripcio = models.CharField(
        max_length=100,
        help_text='Descripci� del subgrup de Moviment'
    )
 
    def __str__(self):
        return '{}'.format(self.descripcio)
    
    def save(self):
        self.descripcio = self.descripcio.upper()
        super(SubgrupMoviment, self).save()

    class Meta:
        verbose_name_plural= "Subgrups de Moviment"
        unique_together = ('grupMoviment','descripcio')
        ordering  = ["descripcio"]
    

class DetallMoviment(ClasseBase):
    subgrupMoviment = models.ForeignKey(SubgrupMoviment, on_delete=models.PROTECT)
    descripcio = models.CharField(
        max_length=100,
        help_text='Descripci� del detall de moviment'
    )

    def __str__(self):
        return '{}'.format(self.descripcio)
    
    def save(self):
        self.descripcio = self.descripcio.upper()
        super(DetallMoviment, self).save()

    class Meta:
        verbose_name_plural= "Detalls de Moviment"
        unique_together = ('subgrupMoviment','descripcio')
        ordering  = ["descripcio"]
    
    
class FormaPagament(ClasseBase):
    descripcio = models.CharField(
        max_length=100,
        help_text='Descripci� de la forma de pagament',
        unique=True
    )
    
    def __str__(self):
        return '{}'.format(self.descripcio)
    
    def save(self):
        self.descripcio = self.descripcio.upper()
        super(FormaPagament, self).save()

    class Meta:
        verbose_name_plural= "Formes de pagament"
        ordering  = ["descripcio"]
    
    
    
class Caixa(ClasseBase):
    descripcio = models.CharField(
        max_length=100,
        help_text='Descripci� de la caixa',
        unique=True
    )
    banc = models.BooleanField(default=True)
    color = models.CharField(default='#FF0000', null=True, blank=True, validators =[validate_color] , max_length=7 )
    usuaris = models.ManyToManyField(User)
    def __str__(self):
        return '{}'.format(self.descripcio)
    
    def save(self):
        self.descripcio = self.descripcio.upper()
        self.color = self.color.upper()
        super(Caixa, self).save()

    class Meta:
        verbose_name_plural= "Caixes"
        ordering  = ["descripcio"]
    
    
