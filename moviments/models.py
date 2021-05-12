from django.db import models

from bases.models import ClasseBase
from mov.models import DetallMoviment, Caixa, FormaPagament



class Moviment(ClasseBase):
    detallMoviment = models.ForeignKey(DetallMoviment, on_delete=models.PROTECT)
    caixa = models.ForeignKey(Caixa, on_delete=models.PROTECT)
    formaPagament = models.ForeignKey(FormaPagament, on_delete=models.PROTECT)
    valor = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Valor del moviment'
        )
    dataMoviment = models.DateField(
        help_text='Data del moviment'
        )

    def __str__(self):
        return '{}:{}:{}:{}:::{}'.format(self.detallMoviment.subgrupMoviment.grupMoviment.descripcio, self.detallMoviment.subgrupMoviment.descripcio, self.detallMoviment.descripcio, self.dataMoviment , self.valor)
    
    def save(self):
        super(Moviment, self).save()

    def copy(self):
        movmimentNew = Moviment()
        movmimentNew.detallMoviment=self.detallMoviment
        movmimentNew.caixa=self.caixa
        movmimentNew.formaPagament=self.formaPagament
        return movmimentNew

    class Meta:
        #ordering = ["-dataMoviment"]
        verbose_name_plural = "Moviments"
        unique_together = ('dataMoviment', 'detallMoviment', 'formaPagament', 'caixa')
        
    
