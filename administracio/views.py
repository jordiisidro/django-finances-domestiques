from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import UserExt

@login_required(login_url='/login/')
def usuari_edit(request, id):
    usuari = User.objects.filter(pk=id).first()
    usuariExt = UserExt.objects.filter(pk=usuari.userext.id).first()
    
    context={}
    template_name="administracio/usuari_edit.html"
    
    if not usuari:
        return redirect("bases:sense_privilegis")
   
    if request.method=='GET':
        if usuari.username!=str(request.user):
            return redirect("bases:sense_privilegis")
        context={'obj':usuari, 'ext':usuariExt}
    if request.method=='POST':
        data = request.POST.copy()
        usuariExt.avatar = data.get('avatar')
        #usuari.set_password(data.get('password'))
        usuari.save()
        usuariExt.save()
        return redirect("moviments:moviment_dash")
    return render(request,template_name,context)   

