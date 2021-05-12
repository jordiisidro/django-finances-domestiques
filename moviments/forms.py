from django import forms

from .models import Moviment
from mov.models import DetallMoviment, SubgrupMoviment, Caixa
from django.forms.utils import ErrorDict
#from django.utils.datastructures import MultiValueDictKeyError

class MovimentForm(forms.ModelForm):
    detallMoviment = forms.DateInput()
    
    class Meta:
        model = Moviment
        fields = [ 'detallMoviment', 'caixa',  'formaPagament', 'valor', 'dataMoviment']
        labels = {'formaPagament': "Forma de pagament"}
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['detallMoviment'].empty_label ="Seleccioni detall de moviment"   
        self.fields['caixa'].empty_label ="Seleccioni caixa"
        self.fields['formaPagament'].empty_label ="Seleccioni forma de pagament"
        
        
    def clean(self):
        #s'ha de crear el detall de moviment
        if not self.data.__getitem__('detallMoviment').isnumeric():
            dm = DetallMoviment()
            dm.descripcio =   self.data.__getitem__('detallMoviment')
            dm.subgrupMoviment =  SubgrupMoviment.objects.all().filter(id=self.data.__getitem__('subgrupMoviment'))[0]
            dm.save()
            self.cleaned_data['detallMoviment']=dm
            self._errors = ErrorDict() #eliminem l'error de no tenir subgrup de moviment
    
        return self.cleaned_data
        
        