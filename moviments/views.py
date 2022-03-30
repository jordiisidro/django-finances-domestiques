import copy
import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum, Min
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


from django.template.defaulttags import register

from bases.views import SensePrivilegis
from mov.models import GrupMoviment, SubgrupMoviment, DetallMoviment, Caixa

from .forms import MovimentForm
from .models import Moviment

from bases import master 
from django.db.models.functions.datetime import ExtractYear




# classes base
class ViewBaseNew(SuccessMessageMixin, SensePrivilegis, generic.CreateView):
    context_object_name = "obj"
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    
    
class ViewBaseEdit(SuccessMessageMixin, SensePrivilegis, generic.UpdateView):
    context_object_name = "obj"
    
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
    
class MovimentView(SensePrivilegis, generic.ListView):
    permission_required = "moviments.view_moviment"
    model = Moviment
    template_name = "moviment/moviment_list.html"
    context_object_name = "obj"
    
    def get_queryset(self):
        return Moviment.objects.select_related('caixa').select_related('detallMoviment__subgrupMoviment__grupMoviment').select_related('formaPagament').filter(usuariCreacio=self.request.user)

    
class MovimentNew(ViewBaseNew):
    permission_required = "moviments.add_moviment"
    model = Moviment
    template_name = "moviment/moviment_form.html"
    form_class = MovimentForm
    success_url = reverse_lazy("moviments:moviment_list")

    def get_context_data(self, **kwargs):
        context = super(MovimentNew, self).get_context_data(**kwargs)
        context["grupsMoviment"] = GrupMoviment.objects.all().order_by("descripcio")
        context["subgrupsMoviment"] = SubgrupMoviment.objects.all().order_by("descripcio")
        context["detallsMoviment"] = DetallMoviment.objects.all().order_by("descripcio")
        context["caixes"] =[]
        for c in Caixa.objects.all():
            if c.usuaris.filter(username= self.request.user).count()>0:
                context["caixes"].append(c)
        
        return context
    
    
    
class MovimentEdit(ViewBaseEdit):
    permission_required = "moviments.change_moviment"
    model = Moviment
    template_name = "moviment/moviment_form.html"
    form_class = MovimentForm
    success_url = reverse_lazy("moviments:moviment_list")
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(MovimentEdit, self).get_context_data(**kwargs)
        context["grupsMoviment"] = GrupMoviment.objects.all().order_by("descripcio")
        context["subgrupsMoviment"] = SubgrupMoviment.objects.all().order_by("descripcio")
        context["detallsMoviment"] = DetallMoviment.objects.all().order_by("descripcio")
        
        context["caixes"] =[]
        for c in Caixa.objects.all():
            if c.usuaris.filter(username= self.request.user).count()>0:
                context["caixes"].append(c)
        context["obj"] = Moviment.objects.filter(pk=pk).first()
        return context


class MovimentDelete(SuccessMessageMixin, generic.DeleteView):
    permission_required = "move.delete_moviment"
    model = Moviment
    template_name = 'moviment/moviment_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy("moviments:moviment_list")
    success_message = "Moviment eliminat correctament"
 
 
@login_required(login_url='/login/')
@permission_required('moviments.add_moviment', login_url='bases:sin_privilegios')
def movimentDuplicate(request, id):
    moviment = Moviment.objects.filter(pk=id).first()
    contexto={}
    form_class = MovimentForm
    movimentNew = Moviment.copy(moviment)
    
    contexto["grupsMoviment"] = GrupMoviment.objects.all().order_by("descripcio")
    contexto["subgrupsMoviment"] = SubgrupMoviment.objects.all().order_by("descripcio")
    contexto["detallsMoviment"] = DetallMoviment.objects.all().order_by("descripcio")
    
    template_name="moviment/moviment_form.html"
    if not moviment:
        return redirect("moviments:moviment_list")
    if request.method=='GET':
        #contexto={'obj':movimentNew, 'dup':True, 'form':form_class}
        contexto["obj"]=movimentNew
        contexto["dup"]= True
        contexto["form"]=form_class
    if request.method=='POST':
        moviment.save()
        return redirect("moviments:moviment_list")
    return render(request,template_name,contexto)    
    
'''   
@login_required(login_url='/login/')
def dashboardMoviments(request, year):
    
    tree = treeMapDespesa(request, year)
    
    # balanç (ingres-despesa)
    balanc = Moviment.objects.filter(Q(usuariCreacio__username=request.user) &  Q(dataMoviment__year=year)  & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')   & ~Q(formaPagament__descripcio='DESPESA ADELA') ).annotate(month=ExtractMonth('dataMoviment')).values('month').annotate(total=Sum('valor'))
    #saldo
    saldo = piesaldo(request)
    
    # despesa  mensual (eliminant els positius)
    despesamensual = Moviment.objects.filter(Q(usuariCreacio__username=request.user) & Q(dataMoviment__year=year) & Q(valor__lt=0) & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')).annotate(month=ExtractMonth('dataMoviment')).values('month', 'detallMoviment__subgrupMoviment__grupMoviment__descripcio').annotate(total=-Sum('valor'))
    # ingrés mensual (tots els positius)
    ingresmensual = Moviment.objects.filter(Q(usuariCreacio__username=request.user) & Q(dataMoviment__year=year) & Q(valor__gt=0) & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')).annotate(month=ExtractMonth('dataMoviment')).values('month', 'detallMoviment__subgrupMoviment__grupMoviment__descripcio').annotate(total=Sum('valor'))
    
    labels = list(range(1, 13))  # inicialitzem amb els 12 mesos
    vBalanc = [0] * 12
    for x in balanc:
        vBalanc[int(x['month']) - 1] = float(x['total'])
    grupsMoviment = list(GrupMoviment.objects.all().values('descripcio', 'color'))
    vDespesa = {}
    for x in grupsMoviment:
        vDespesa[x['descripcio']] = [[x['color']],[0] * 12]
        
    vIngres = copy.deepcopy(vDespesa)
    
    for x in despesamensual:
        vDespesa[x['detallMoviment__subgrupMoviment__grupMoviment__descripcio']][1][int(x['month']) - 1] = float(x['total'])
   
    
    for x in ingresmensual:
        vIngres[x['detallMoviment__subgrupMoviment__grupMoviment__descripcio']][1][int(x['month']) - 1] = float(x['total'])
    
    m = list(Moviment.objects.filter(Q(dataMoviment__year=year))
        .values('detallMoviment__subgrupMoviment__grupMoviment__descripcio').annotate(total=Sum('valor'))
        )
    labels2 = [] 
    values2 = []
    for x in m:
        labels2.append(x['detallMoviment__subgrupMoviment__grupMoviment__descripcio'])  
        values2.append(float(x['total']))
        
    
    
    context = {}
    template_name = "moviment/moviment_dashboard.html"
        
    if request.method == 'GET':
        context = { 'mesLabels':labels, 'vBalanc':vBalanc, 'vDespesa':vDespesa, 'vIngres':vIngres,
                   'saldoLabel':saldo[0], 'saldoColor':saldo[1], 'saldoValues': saldo[2],
                   'treeLabels':tree[0],'treeParents':tree[1], 'treeValues':tree[2], 'treeText':tree[3], 'treeColor': tree[4]
                   }
        
    # if request.method=='POST':
        
        # messages.success(request, 'Grup de moviment desactivat')
        # return redirect("mov:grupMoviment_list")
    return render(request, template_name, context)   
''' 

def piesaldo(request):
    saldo = Moviment.objects.\
        filter(Q(usuariCreacio__username=request.user)  & ~Q(detallMoviment__descripcio__exact='SALDO ESTATIC')   & ~Q(formaPagament__descripcio='DESPESA ADELA') ).\
        values('caixa__descripcio').\
        annotate(total=Sum('valor'), col=Min('caixa__color'))
    saldoLabel = []
    saldoValues = []
    saldoColor = []
    for x in saldo:
        saldoLabel.append(x['caixa__descripcio'])
        saldoValues.append(float(x['total']))
        saldoColor.append(x['col'])
    return [saldoLabel, saldoColor, saldoValues]

@login_required(login_url='/login/')
def treeMapDespesa(request, dataInici=str(master.firstDateCurrentYear), dataFi=str(master.lastDateCurrentYear)):

           
    grupsMoviment = list(GrupMoviment.objects.all().values('descripcio', 'color','id'))
    subgrupsMoviment = list(SubgrupMoviment.objects.all().values('descripcio','grupMoviment__descripcio','id'))
    detallsMoviment = list(DetallMoviment.objects.all().values('descripcio', 'subgrupMoviment__descripcio', 'subgrupMoviment__grupMoviment__descripcio', 'id'))
    
    val = Moviment.objects.filter(Q(usuariCreacio__username=request.user) & Q(dataMoviment__gte=dataInici)  & Q(dataMoviment__lte=dataFi)   & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')  ).values('detallMoviment__id').annotate(total=Sum('valor'))
    dval ={}
    for x in val:
        dval[x['detallMoviment__id']]=float(x['total'])
    
    val = Moviment.objects.filter(Q(usuariCreacio__username=request.user) & Q(dataMoviment__gte=dataInici)  & Q(dataMoviment__lte=dataFi)  & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')  ).values('detallMoviment__subgrupMoviment__id').annotate(total=Sum('valor'))
    sgval ={}
    for x in val:
        sgval[x['detallMoviment__subgrupMoviment__id']]=float(x['total'])
    
    val = Moviment.objects.filter(Q(usuariCreacio__username=request.user) & Q(dataMoviment__gte=dataInici)  & Q(dataMoviment__lte=dataFi) & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')  ).values('detallMoviment__subgrupMoviment__grupMoviment__id').annotate(total=Sum('valor'))
    gval ={}
    for x in val:
        gval[x['detallMoviment__subgrupMoviment__grupMoviment__id']]=float(x['total'])
    
    labels = []
    parents = []
    values = []
    text = []
    colors = []
    for x in grupsMoviment:
        labels.append(x['descripcio'])
        parents.append("")
        values.append(0)
        if x['id'] in gval:
            text.append(-gval[x['id']])
        else:
            text.append(0)
        colors.append(x['color'])
            
    for x in subgrupsMoviment:
        labels.append(x['grupMoviment__descripcio']+'-'+x['descripcio'])
        parents.append(x['grupMoviment__descripcio'])
        values.append(0)
        if x['id'] in sgval:
            text.append(-sgval[x['id']])
        else:
            text.append(0)
        
        
    for x in detallsMoviment:
        labels.append(x['subgrupMoviment__grupMoviment__descripcio']+'-'+x['subgrupMoviment__descripcio']+'-'+x['descripcio'])
        parents.append(x['subgrupMoviment__grupMoviment__descripcio']+'-'+x['subgrupMoviment__descripcio'])
        if x['id'] in dval:
            values.append(-dval[x['id']])
            text.append(-dval[x['id']])
        else:
            values.append(0)
            text.append(0)
              
    #return [labels, parents, values, text, colors]
    context = {}
    template_name = "moviment/moviment_dashboard_tree.html"
        
   #datetime.datetime.strptime(dataInici, "%Y-5m-%d").date()     
    if request.method == 'GET':
        context = {'treeLabels':labels,'treeParents':parents, 'treeValues':values, 'treeText':text, 'treeColor': colors, 'dataInici':datetime.datetime.strptime(dataInici, "%Y-%m-%d").date(), 'dataFi': datetime.datetime.strptime(dataFi, "%Y-%m-%d").date()
                   }
    return render(request, template_name, context)  


def balanc( request, year, data):
    # balanç (ingres-despesa)
    balanc = Moviment.objects.\
        filter(Q(usuariCreacio__username=request.user) &  Q(dataMoviment__year__lte=year)  & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')   & ~Q(formaPagament__descripcio='DESPESA ADELA') ).\
        annotate(month=ExtractMonth('dataMoviment'), year=ExtractYear('dataMoviment')).\
        values('month','year').\
        annotate(total=Sum('valor')).\
        order_by('year','month')
    for x in balanc:
        data[master.months[int(x['month'])]+'-'+str(x['year'])] = float(x['total'])
    return data
        


@login_required(login_url='/login/')
def dashboardMoviments2(request):
    
    year=master.currentYear
    lastyear=master.lastYear
    #saldo
    saldo = piesaldo(request)
    
    data={}
    labels =[]
    labelsPos = {}
    for x in range(0,13):
        month = master.currentMonth+x-12 if master.currentMonth+x>12  else master.currentMonth+x
        labels.append(master.months[month]+'-'+ str(master.currentYear-1 if month>=master.currentMonth and x<12 else master.currentYear))
        labelsPos[master.months[month]+'-'+ str(master.currentYear-1 if month>=master.currentMonth and x<12 else master.currentYear)]=x
        data[master.months[month]+'-'+ str(master.currentYear-1 if month>=master.currentMonth and x<12 else master.currentYear)]=0
       
   
    data = balanc(request, year, data)
    
    
    # despesa  mensual (eliminant els positius)
    despesamensual = Moviment.objects.\
        filter(Q(usuariCreacio__username=request.user) & (Q(dataMoviment__year__exact=year) | Q(dataMoviment__year__exact=lastyear) & Q(dataMoviment__month__gte=master.currentMonth)) & Q(valor__lt=0) & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')).\
        annotate(month=ExtractMonth('dataMoviment'), year=ExtractYear('dataMoviment')).\
        values('month', 'year', 'detallMoviment__subgrupMoviment__grupMoviment__descripcio').\
        annotate(total=-Sum('valor')).\
        order_by('year','month')
    # ingrés mensual (tots els positius)
    ingresmensual = Moviment.objects.\
        filter(Q(usuariCreacio__username=request.user) &  (Q(dataMoviment__year__exact=year) | Q(dataMoviment__year__exact=lastyear) & Q(dataMoviment__month__gte=master.currentMonth))& Q(valor__gt=0) & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')   & ~Q(detallMoviment__descripcio__exact='SALDO INICIAL')).\
        annotate(month=ExtractMonth('dataMoviment'), year=ExtractYear('dataMoviment')).\
        values('month', 'year','detallMoviment__subgrupMoviment__grupMoviment__descripcio').\
        annotate(total=Sum('valor')).\
        order_by('detallMoviment__subgrupMoviment__grupMoviment__descripcio','year','month')
    
    grupsMoviment = list(GrupMoviment.objects.all().values('descripcio', 'color'))
    vDespesa = {}
    for x in grupsMoviment:
        vDespesa[x['descripcio']] = [[x['color']],[0] * 13]
    
    vIngres = copy.deepcopy(vDespesa)
    
    for x in despesamensual:
        vDespesa[x['detallMoviment__subgrupMoviment__grupMoviment__descripcio']][1][labelsPos[master.months[int(x['month'])]+'-'+str(x['year'])]] = float(x['total'])
        
    
    for x in ingresmensual:
        vIngres[x['detallMoviment__subgrupMoviment__grupMoviment__descripcio']][1][labelsPos[master.months[int(x['month'])]+'-'+str(x['year'])]] = float(x['total'])
    
    context = {}
    template_name = "moviment/moviment_dashboard.html"
    
    if request.method == 'GET':
        context = { 'mesLabels':labels, 'vBalanc':list(data.values()), 
                   'vDespesa':vDespesa, 'vIngres':vIngres,
                   'saldoLabel':saldo[0], 'saldoColor':saldo[1], 'saldoValues': saldo[2],
                   }
        
    return render(request, template_name, context)  




@login_required(login_url='/login/')
def dashboardSaldo(request, year=master.currentYear, month=master.currentMonth):
    caixes = []
    for c in Caixa.objects.all():
        if c.usuaris.filter(username= request.user).count()>0:
            caixes.append(c)
    
    vSaldo = {}
    vSaldoPerc = {}
    for c in caixes:
        obj = {}
        obj['color']=c.color
        obj['data']=[0]*13
        obj['banc']=c.banc
        vSaldo[c.descripcio]=obj
        
        
    vSaldoPerc = copy.deepcopy(vSaldo)
    data={}
    labels =[]
    labelsPos = {}
    for x in range(0,13):
        monthCalc = month+x-12 if month+x>12  else month+x
        yearCalc = year-1 if monthCalc>=month and x<12 else year
        
        labels.append(master.months[monthCalc]+'-'+ str(yearCalc))
        labelsPos[master.months[monthCalc]+'-'+ str(yearCalc)]=x
        data[master.months[monthCalc]+'-'+ str(yearCalc)]=0
        
        sal = Moviment.objects.\
                      filter(Q(usuariCreacio__username=request.user)  & ~Q(detallMoviment__descripcio__exact='SALDO ESTATIC')   & ~Q(formaPagament__descripcio='DESPESA ADELA') & Q(dataMoviment__lte=datetime.date(yearCalc, monthCalc, 1)+ relativedelta(months=1)+ relativedelta(days=-1)) ).\
                      values('caixa__descripcio').\
                      annotate(total=Sum('valor')
        )
        
        
        salest = Moviment.objects.\
                      filter(Q(usuariCreacio__username=request.user)  & Q(detallMoviment__descripcio__exact='SALDO ESTATIC') & Q(dataMoviment__lte=datetime.date(yearCalc, monthCalc, 1)+ relativedelta(months=1)+ relativedelta(days=-1)) & Q(dataMoviment__gte=datetime.date(yearCalc, monthCalc, 1)+ relativedelta(months=0)+ relativedelta(days=0)) ).\
                      values('caixa__descripcio').\
                      annotate(total=Sum('valor')
        )
        
        subtotal = 0
        for cai in salest:
            vSaldo[cai['caixa__descripcio']]['data'][x]=f"{cai['total']:.2f}"
            subtotal += Decimal(cai['total'])
        
        for cai in salest:
            vSaldoPerc[cai['caixa__descripcio']]['data'][x]=f"{100*cai['total']/subtotal:.2f}"    
        
        subtotal = 0
        for cai in sal:
            vSaldo[cai['caixa__descripcio']]['data'][x]=f"{cai['total']:.2f}"
            subtotal += Decimal(cai['total'])
            
        for cai in sal:
            vSaldoPerc[cai['caixa__descripcio']]['data'][x]=f"{100*cai['total']/subtotal:.2f}"
            

    
    context = {}
    template_name = "moviment/moviment_dashboard_saldo.html"
    if request.method == 'GET':
        context = { 'mesLabels':labels, 
                   'vSaldo':vSaldo,
                   'vSaldoPerc':vSaldoPerc,
                   'mesNumber': list(range(0,13)),
                   'year':year, 
                   'month':month,
                   'lblMesos':master.months
                   }
        
    return render(request, template_name, context)  



@login_required(login_url='/login/')
def dashboardDespesa(request, year=master.currentYear, month=master.currentMonth):
    labels =[]
    labelsPos = {}
    for x in range(0,13):
        m = month+x-12 if month+x>12  else month+x
        labels.append(master.months[m]+'-'+ str(year-1 if m>=month and x<12 else year))
        labelsPos[master.months[m]+'-'+ str(year-1 if m>=month and x<12 else year)]=x
     
     
    despesamensual = Moviment.objects.\
        filter(Q(usuariCreacio__username=request.user) 
            & Q(dataMoviment__lte=datetime.date(year, month, 1)+ relativedelta(months=1)+ relativedelta(days=-1)) 
            & Q(dataMoviment__gte=datetime.date(year-1, month, 1)+ relativedelta(months=1)+ relativedelta(days=-1)) 
            & Q(valor__lt=0) 
            & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')).\
        annotate(month=ExtractMonth('dataMoviment'), year=ExtractYear('dataMoviment')).\
        values('month', 'year', 'detallMoviment__subgrupMoviment__grupMoviment__descripcio').\
        annotate(total=-Sum('valor')).\
        order_by('year','month')
    
    despesamensualSubgrup =[]
    
    despesamensualSubgrup = Moviment.objects.\
        filter(Q(usuariCreacio__username=request.user) 
        & Q(dataMoviment__lte=datetime.date(year, month, 1)+ relativedelta(months=1)+ relativedelta(days=-1)) 
        & Q(dataMoviment__gte=datetime.date(year-1, month, 1)+ relativedelta(months=1)+ relativedelta(days=-1)) 
        & Q(valor__lt=0) 
        & ~Q(detallMoviment__subgrupMoviment__grupMoviment__descripcio__exact='TRASPÀS COMPTES')).\
        annotate(month=ExtractMonth('dataMoviment'), year=ExtractYear('dataMoviment')).\
        values('month', 'year', 'detallMoviment__subgrupMoviment__grupMoviment__descripcio', 'detallMoviment__subgrupMoviment__descripcio').\
        annotate(total=-Sum('valor')).\
        order_by('year','month')
    
    grupsMoviment = list(GrupMoviment.objects.all().values('descripcio', 'color'))
    vDespesa = {}
    vDespesaSubgrup = {}
    for x in grupsMoviment:
        vDespesa[x['descripcio']] = [[x['color']],[0] * 13]
        subgrupsMoviment = list(SubgrupMoviment.objects.filter(Q(grupMoviment__descripcio=x['descripcio']  )))
        
        vDespesaSubgrup[x['descripcio']]={}
        for y in subgrupsMoviment:
            vDespesaSubgrup[x['descripcio']][y.descripcio]= [[0] * 13]
    
    for x in despesamensual:
        vDespesa[x['detallMoviment__subgrupMoviment__grupMoviment__descripcio']][1][labelsPos[master.months[int(x['month'])]+'-'+str(x['year'])]] = float(x['total'])
        
    
    for x in despesamensualSubgrup:
        vDespesaSubgrup[x['detallMoviment__subgrupMoviment__grupMoviment__descripcio']][x['detallMoviment__subgrupMoviment__descripcio']][0][labelsPos[master.months[int(x['month'])]+'-'+str(x['year'])]] = float(x['total'])
        
    
    context = {}
    template_name = "moviment/moviment_dashboard_despesa.html"
    
        
    if request.method == 'GET':
        context = { 'mesLabels':labels, 
                   'vDespesa':vDespesa,
                   'vDespesaSubgrup':vDespesaSubgrup,
                   'year':year, 
                   'month':month,
                   'lblMesos':master.months 
                   }
        
    return render(request, template_name, context)  


'''
FILTERS
'''

 
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)[1]


@register.filter
def get_firstDictPosition(dictionary):
    return next(iter(dictionary))


@register.filter
def get_itemList(list, position):
    return list[position]

@register.filter
def equals(a,b):
    return a==b


@register.filter
def get_color(dictionary, key):
    return dictionary.get(key)[0][0]



@register.filter
def get_color2(dictionary, key):
    return dictionary.get(key)['color']


@register.filter
def get_banc(dictionary, key):
    return dictionary.get(key)['banc']

@register.filter
def get_data(dictionary, key):
    return dictionary.get(key)['data']


@register.filter
def get_keys(dictionary, key):
    return list(dictionary.get(key).keys())


@register.filter
def get_values(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_values_list(dictionary, key):
    return dictionary.get(key)[0]



@register.filter
def get_dataTotal(dictionary, mes=12):
    val = 0.0
    for x in dictionary:
        val +=float(dictionary.get(x)['data'][mes])
    return val


@register.filter
def get_dataTotalBanc(dictionary, mes=12):
    val = 0.0
    for x in dictionary:
        if dictionary.get(x)['banc']:
            val +=float(dictionary.get(x)['data'][mes])
    return val

@register.filter
def get_mes(idMes):
    return master.months.get(idMes)
