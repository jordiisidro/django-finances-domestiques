from django import forms

import re

from .models import GrupMoviment, SubgrupMoviment, DetallMoviment, FormaPagament, Caixa


class GrupMovimentForm(forms.ModelForm):
    class Meta:
        model = GrupMoviment
        fields = ['descripcio', 'color','estat']
        labels = {'descripció': "Descripció del grup de moviment",
                  'estat': 'Estat'}
        widget = {'descripcio': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


    def clean(self):
        try:
            sc = GrupMoviment.objects.get(
                descripcio=self.cleaned_data["descripcio"].upper()
            )
            rg = re.compile("#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]")
            color1 = self.cleaned_data["color"].upper()
            if not self.instance.pk:
                raise forms.ValidationError("Clau primària duplicada")
            elif self.instance.pk!=sc.pk:
                raise forms.ValidationError("Descripció duplicada")
            elif rg.match(color1)==None:
                raise forms.ValidationError('Format de color incorrecte',   code='invalid',)
        except GrupMoviment.DoesNotExist:
            pass
        
        return self.cleaned_data
      
            
class SubgrupMovimentForm(forms.ModelForm):
    class Meta:
        model = SubgrupMoviment
        fields = ['grupMoviment', 'descripcio', 'estat']
        labels = {'descripció': "Descripció del subgrup de moviment",
                  "estat": "Estat"}
        widget = {'descripcio': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['grupMoviment'].empty_label ="Seleccioni grup de moviment"
        
    def clean(self):
        try:
            sc = SubgrupMoviment.objects.get(
                descripcio=self.cleaned_data["descripcio"].upper(),  grupMoviment=self.cleaned_data["grupMoviment"]
            )
            if not self.instance.pk:
                raise forms.ValidationError("Clau primària duplicada")
            elif self.instance.pk!=sc.pk:
                raise forms.ValidationError("Descripció duplicada")
        except SubgrupMoviment.DoesNotExist:
            pass
        
        return self.cleaned_data
        
   
class DetallMovimentForm(forms.ModelForm):
    class Meta:
        model = DetallMoviment
        fields = [ 'subgrupMoviment', 'descripcio', 'estat']
        labels = {'descripció': "Descripció del subgrup de moviment",
                  "estat": "Estat"}
        widget = {'descripcio': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['subgrupMoviment'].empty_label ="Seleccioni subgrup de moviment"   
        
    def clean(self):
        try:
            sc = DetallMoviment.objects.get(
                descripcio=self.cleaned_data["descripcio"].upper(), subgrupMoviment=self.cleaned_data["subgrupMoviment"]
            )
            if not self.instance.pk:
                raise forms.ValidationError("Clau primària duplicada")
            elif self.instance.pk!=sc.pk:
                raise forms.ValidationError("Descripció duplicada")
        except DetallMoviment.DoesNotExist:
            pass
        
        return self.cleaned_data    
     
        
class FormaPagamentForm(forms.ModelForm):
    class Meta:
        model = FormaPagament
        fields = ['descripcio', 'estat']
        labels = {'descripció': "Descripció de la forma de pagament",
                  "estat": "Estat"}
        widget = {'descripcio': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
            
    def clean(self):
        try:
            sc = FormaPagament.objects.get(
                descripcio=self.cleaned_data["descripcio"].upper()
            )
            if not self.instance.pk:
                raise forms.ValidationError("Clau primària duplicada")
            elif self.instance.pk!=sc.pk:
                raise forms.ValidationError("Descripció duplicada")
        except FormaPagament.DoesNotExist:
            pass
        
        return self.cleaned_data
            
            
class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['descripcio', 'color', 'banc', 'estat']
        labels = {'descripció': "Descripció de la caixa",
                  "estat": "Estat"}
        widget = {'descripcio': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
            
    def clean(self):
        try:
            sc = Caixa.objects.get(
                descripcio=self.cleaned_data["descripcio"].upper()
            )
            rg = re.compile("#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]")
            color1 = self.cleaned_data["color"].upper()
            
            if not self.instance.pk:
                raise forms.ValidationError("Clau primària duplicada")
            elif self.instance.pk!=sc.pk:
                raise forms.ValidationError("Descripció duplicada")
            elif rg.match(color1)==None:
                raise forms.ValidationError('Format de color incorrecte',   code='invalid',)
        except Caixa.DoesNotExist:
            pass
        
        return self.cleaned_data
    
    
class CaixaFormUsuaris(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['usuaris']
        widget = {'usuaris': forms.MultipleChoiceField}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
            
    def clean(self):
        '''
        try:
            sc = Caixa.objects.get(
                descripcio=self.cleaned_data["descripcio"].upper()
            )
            rg = re.compile("#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]")
            color1 = self.cleaned_data["color"].upper()
            
            if not self.instance.pk:
                raise forms.ValidationError("Clau primària duplicada")
            elif self.instance.pk!=sc.pk:
                raise forms.ValidationError("Descripció duplicada")
            elif rg.match(color1)==None:
                raise forms.ValidationError('Format de color incorrecte',   code='invalid',)
        except Caixa.DoesNotExist:
            pass
        '''
        return self.cleaned_data