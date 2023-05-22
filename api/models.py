from django.db import models
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from accounts.models import User


class Products(models.Model):
    name = models.CharField(max_length=128, unique=True)
    stock = models.IntegerField(default=0)
    sell_price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Control_Period(models.Model):
    start_date = models.DateField(null=False)
    close_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.start_date)


class Motagrat(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField(auto_now_add=True)
    control_period = models.ForeignKey(Control_Period, on_delete=models.CASCADE)

    @property
    def control_period_date(self):
        return self.control_period.start_date

    @property
    def control_period_state(self):
        return self.control_period.active

    def __str__(self):
        return self.name


class Motagrat_Products(models.Model):
    product = models.ForeignKey(Products, models.CASCADE)
    motagra = models.ForeignKey(Motagrat, models.CASCADE)
    qty = models.PositiveIntegerField()
    pieces = models.PositiveIntegerField()
    piece_price = models.FloatField()
    buy_price = models.FloatField()
    profit = models.FloatField()

    def __str__(self):
        return self.motagra.name

    class Meta:
        unique_together = ('product', 'motagra')

    @property
    def product_name(self):
        return self.product.name

    @property
    def total_buy_price_value(self):
        return Motagrat_Products.objects.aggregate(Sum('buy_price'))

    @property
    def total_profit_value(self):
        return Motagrat_Products.objects.aggregate(Sum('profit'))
    @property
    def total_pieces_for_product(self):
        return self.qty * self.pieces
    @property
    def total_sell_price_value(self):
        return self.pieces * self.qty * self.piece_price


PAYMENTTYPES = ((1, 'كاش'),
                (2, 'تأريشة'),)


class User_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now=True)
    payment_type = models.CharField(choices=PAYMENTTYPES, max_length=6)

    def __str__(self):
        return self.user_id.name

