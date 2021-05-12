from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy


from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required


from .models import GrupMoviment, SubgrupMoviment, DetallMoviment, FormaPagament, Caixa
from .forms import GrupMovimentForm, SubgrupMovimentForm, DetallMovimentForm, FormaPagamentForm, CaixaForm, CaixaFormUsuaris

from django.contrib.auth.models import User

from bases.views import SensePrivilegis

from django.template.defaulttags import register



#classes base
class ViewBaseNew(SuccessMessageMixin, SensePrivilegis,  generic.CreateView):
    context_object_name = "obj"
    #success_message="Registre creat correctament"
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    
    
class ViewBaseEdit(SuccessMessageMixin, SensePrivilegis,  generic.UpdateView):
    context_object_name = "obj"
    #success_message="Registre actualitzat correctament"
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
    

class GrupMovimentView( SensePrivilegis, generic.ListView):
    permission_required = "mov.view_grupmoviment"
    model = GrupMoviment
    template_name = "mov/grupMoviment_list.html"
    context_object_name = "obj"

    
class GrupMovimentNew(ViewBaseNew):
    permission_required="mov.add_grupmoviment"
    model=GrupMoviment
    template_name="mov/grupMoviment_form.html"
    form_class=GrupMovimentForm
    success_url=reverse_lazy("mov:grupMoviment_list")
    

    
class GrupMovimentEdit(ViewBaseEdit):
    permission_required="mov.change_grupmoviment"
    model=GrupMoviment
    template_name="mov/grupMoviment_form.html"
    form_class=GrupMovimentForm
    success_url=reverse_lazy("mov:grupMoviment_list")


class GrupMovimentDelete(SuccessMessageMixin, generic.DeleteView):
    permission_required="mov.delete_grupmoviment"
    model=GrupMoviment
    template_name='mov/cataleg_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("mov:grupMoviment_list")
    success_message="Grup de moviment eliminat correctament"
    
    
@login_required(login_url='/login/')
@permission_required('mov.change_grupmoviment', login_url='bases:sense_privilegis')
def grupMoviment_inactivar(request, id):
    grupMoviment = GrupMoviment.objects.filter(pk=id).first()
    contexto={}
    template_name="mov/grupMoviment_inactivar.html"
    if not grupMoviment:
        return redirect("mov:grupMoviment_list")
   
    if request.method=='GET':
        contexto={'obj':grupMoviment}
    if request.method=='POST':
        grupMoviment.estat=False
        grupMoviment.save()
        #messages.success(request, 'Grup de moviment desactivat')
        return redirect("mov:grupMoviment_list")
    return render(request,template_name,contexto)   







class SubgrupMovimentView( SensePrivilegis, generic.ListView):
    permission_required = "mov.view_subgrupmoviment"
    model = SubgrupMoviment
    template_name = "mov/subgrupMoviment_list.html"
    context_object_name = "obj"

    
class SubgrupMovimentNew(ViewBaseNew):
    permission_required="mov.add_subgrupmoviment"
    model=SubgrupMoviment
    template_name="mov/subgrupMoviment_form.html"
    form_class=SubgrupMovimentForm
    success_url=reverse_lazy("mov:subgrupMoviment_list")

    
class SubgrupMovimentEdit(ViewBaseEdit):
    permission_required="move.change_subgrupmoviment"
    model=SubgrupMoviment
    template_name="mov/subgrupMoviment_form.html"
    form_class=SubgrupMovimentForm
    success_url=reverse_lazy("mov:subgrupMoviment_list")


class SubgrupMovimentDelete(SuccessMessageMixin, generic.DeleteView):
    permission_required="mov.delete_subgrupmoviment"
    model=SubgrupMoviment
    template_name='mov/cataleg_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("mov:subgrupMoviment_list")
    success_message="Subgrup de moviment eliminat correctament"
    
    
@login_required(login_url='/login/')
@permission_required('mov.change_subgrupmoviment', login_url='bases:sense_privilegis')
def subgrupMoviment_inactivar(request, id):
    subgrupMoviment = SubgrupMoviment.objects.filter(pk=id).first()
    contexto={}
    template_name="mov/subgrupMoviment_inactivar.html"
    if not subgrupMoviment:
        return redirect("mov:subgrupMoviment_list")
   
    if request.method=='GET':
        contexto={'obj':subgrupMoviment}
    if request.method=='POST':
        subgrupMoviment.estat=False
        subgrupMoviment.save()
        #messages.success(request, 'Grup de moviment desactivat')
        return redirect("mov:subgrupMoviment_list")
    return render(request,template_name,contexto)   





class DetallMovimentView( SensePrivilegis, generic.ListView):
    permission_required = "mov.view_detallmoviment"
    model = DetallMoviment
    template_name = "mov/detallMoviment_list.html"
    context_object_name = "obj"

    
class DetallMovimentNew(ViewBaseNew):
    permission_required="mov.add_detallmoviment"
    model=DetallMoviment
    template_name="mov/detallMoviment_form.html"
    form_class=DetallMovimentForm
    success_url=reverse_lazy("mov:detallMoviment_list")
    
    def get_context_data(self, **kwargs):
        context = super(DetallMovimentNew, self).get_context_data(**kwargs)
        context["grupsMoviment"] = GrupMoviment.objects.all().order_by("descripcio")
        context["subgrupsMoviment"] = SubgrupMoviment.objects.all().order_by("descripcio")
        return context


class DetallMovimentEdit(ViewBaseEdit):
    permission_required="move.change_detallmoviment"
    model=DetallMoviment
    template_name="mov/detallMoviment_form.html"
    form_class=DetallMovimentForm
    success_url=reverse_lazy("mov:detallMoviment_list")
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(DetallMovimentEdit, self).get_context_data(**kwargs)
        context["grupsMoviment"] = GrupMoviment.objects.all().order_by("descripcio")
        context["subgrupsMoviment"] = SubgrupMoviment.objects.all().order_by("descripcio")
        context["obj"] = DetallMoviment.objects.filter(pk=pk).first()
        return context


class DetallMovimentDelete(SuccessMessageMixin, generic.DeleteView):
    permission_required="mov.delete_detallmoviment"
    model=DetallMoviment
    template_name='mov/cataleg_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("mov:detallMoviment_list")
    success_message="Detall de moviment eliminat correctament"
    
    
@login_required(login_url='/login/')
@permission_required('mov.change_detallmoviment', login_url='bases:sense_privilegis')
def detallMoviment_inactivar(request, id):
    detallMoviment = DetallMoviment.objects.filter(pk=id).first()
    contexto={}
    template_name="mov/detallMoviment_inactivar.html"
    if not detallMoviment:
        return redirect("mov:detallMoviment_list")
   
    if request.method=='GET':
        contexto={'obj':detallMoviment}
    if request.method=='POST':
        detallMoviment.estat=False
        detallMoviment.save()
        #messages.success(request, 'Grup de moviment desactivat')
        return redirect("mov:detallMoviment_list")
    return render(request,template_name,contexto)   




class FormaPagamentView( SensePrivilegis, generic.ListView):
    permission_required = "mov.view_formapagament"
    model = FormaPagament
    template_name = "mov/formaPagament_list.html"
    context_object_name = "obj"

    
class FormaPagamentNew(ViewBaseNew):
    permission_required="mov.add_formapagament"
    model=FormaPagament
    template_name="mov/formaPagament_form.html"
    form_class=FormaPagamentForm
    success_url=reverse_lazy("mov:formaPagament_list")

    
class FormaPagamentEdit(ViewBaseEdit):
    permission_required="move.change_formapagament"
    model=FormaPagament
    template_name="mov/formaPagament_form.html"
    form_class=FormaPagamentForm
    success_url=reverse_lazy("mov:formaPagament_list")


class FormaPagamentDelete(SuccessMessageMixin, generic.DeleteView):
    permission_required="mov.delete_formapagament"
    model=FormaPagament
    template_name='mov/cataleg_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("mov:formaPagament_list")
    success_message="Forma de pagament correctament"
    
    
@login_required(login_url='/login/')
@permission_required('mov.change_formapagament', login_url='bases:sense_privilegis')
def formaPagament_inactivar(request, id):
    formaPagament = FormaPagament.objects.filter(pk=id).first()
    contexto={}
    template_name="mov/formaPagament_inactivar.html"
    if not formaPagament:
        return redirect("mov:formaPagament_list")
   
    if request.method=='GET':
        contexto={'obj':formaPagament}
    if request.method=='POST':
        formaPagament.estat=False
        formaPagament.save()
        #messages.success(request, 'Grup de moviment desactivat')
        return redirect("mov:formaPagament_list")
    return render(request,template_name,contexto)   






class CaixaView( SensePrivilegis, generic.ListView):
    permission_required = "mov.view_caixa"
    model = Caixa
    template_name = "mov/caixa_list.html"
    context_object_name = "obj"
    
    
class CaixaNew(ViewBaseNew):
    permission_required="mov.add_caixa"
    model=Caixa
    template_name="mov/caixa_form.html"
    form_class=CaixaForm
    success_url=reverse_lazy("mov:caixa_list")

    
class CaixaEdit(ViewBaseEdit):
    permission_required="mov.change_caixa"
    model=Caixa
    template_name="mov/caixa_form.html"
    form_class=CaixaForm
    success_url=reverse_lazy("mov:caixa_list")


class CaixaDelete(SuccessMessageMixin, generic.DeleteView):
    permission_required="mov.delete_caixa"
    model=Caixa
    template_name='mov/cataleg_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("mov:caixa_list")
    success_message="Caixa eliminada correctament"
    
    
@login_required(login_url='/login/')
@permission_required('mov.change_caixa', login_url='bases:sebse_privilegis')
def caixa_inactivar(request, id):
    caixa = Caixa.objects.filter(pk=id).first()
    contexto={}
    template_name="mov/caixa_inactivar.html"
    if not caixa:
        return redirect("mov:caixa_list")
   
    if request.method=='GET':
        contexto={'obj':caixa}
    if request.method=='POST':
        caixa.estat=False
        caixa.save()
        #messages.success(request, 'Grup de moviment desactivat')
        return redirect("mov:caixa_list")
    return render(request,template_name,contexto)   





@login_required(login_url='/login/')
@permission_required('mov.change_caixa', login_url='bases:sense_privilegis')
def caixa_usuaris(request, id):
    caixa = Caixa.objects.filter(pk=id).first()
    user = User.objects.all()
    contexto={}
    template_name="mov/caixa_usuaris.html"
    if not caixa:
        return redirect("mov:caixa_list")
   
    if request.method=='GET':
        contexto={'obj':caixa, 'usr':user}
    if request.method=='POST':
        caixa.save()
        #caixa.usuaris.remove(p2)
        #caixa.usuaris.remove(add)
        caixa.usuaris.clear()
        for u in request.POST.getlist("usuaris"):
            user = User.objects.all().filter(id=u)
            caixa.usuaris.add(u)
        return redirect("mov:caixa_list")
    return render(request,template_name,contexto)   



@login_required(login_url='/login/')
@permission_required('mov.change_caixa', login_url='bases:sense_privilegis')
def caixa_usuari_canvia_estat(request, id):
    caixa = Caixa.objects.filter(pk=id).first()
    contexto={}
    template_name="mov/caixa_usuaris_self.html"
    if not caixa:
        return redirect("mov:caixa_list")
   
    if request.method=='GET':
        contexto={'obj':caixa}
    if request.method=='POST':
        caixa.save()
        if caixa.usuaris.filter(username =request.user ).count()>0:
            caixa.usuaris.remove(request.user)
        else:
            caixa.usuaris.add(request.user)
        return redirect("mov:caixa_list")
    return render(request,template_name,contexto)   



@register.filter
def is_username(queryset, username):
    for x in queryset.values('id','username'):
        if x['username'] ==username:
            return True
    return False
    
