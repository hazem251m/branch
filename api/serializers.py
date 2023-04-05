from rest_framework import serializers
from .models import Products, Control_Period, Motagrat, Motagrat_Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

    read_only_fields = ('id',)


class ControlPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control_Period
        fields = "__all__"


class MotagratSerializer(serializers.ModelSerializer):
    start_date = serializers.ReadOnlyField(source='control_period.start_date')
    active = serializers.ReadOnlyField(source='control_period.active')

    class Meta:
        model = Motagrat
        fields = "__all__"


class MotagratProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motagrat_Products
        fields = "__all__"


class MotagraProductsDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Motagrat_Products
        fields = ["product_name", "qty", "pieces", "piece_price", "buy_price", "sell_price", "profit"]


class AvailableProductsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    stock = serializers.IntegerField()
    sell_price = serializers.FloatField()
