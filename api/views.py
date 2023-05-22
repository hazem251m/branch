from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Products, Control_Period, Motagrat, Motagrat_Products
from .serializers import ProductsSerializer, ControlPeriodSerializer, MotagratSerializer, MotagratProductsSerializer, \
    MotagraProductsDetailSerializer, AvailableProductsSerializer


class ProductListApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
        }
        product_serializer = ProductsSerializer(data=data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_object(self, product_id):
        try:
            return Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return None

    def get(self, request, product_id, *args, **kwargs):
        product = self.get_object(product_id=product_id)
        if not product:
            return Response(
                {"message": "product doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ProductsSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id, *args, **kwargs):
        product = self.get_object(product_id=product_id)
        if not product:
            return Response(
                {"message": "Object with product id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        product.delete()
        return Response(
            {"message": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class ControlPeriodListView(APIView):
    def check_last_period(self, request):
        last_period = Control_Period.objects.last()
        if last_period:
            last_period.active = False
            last_period.close_date = datetime.today()
            last_period.save()
            return last_period

    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        periods = Control_Period.objects.all()
        serializer = ControlPeriodSerializer(periods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        date = request.data
        data = {
            'start_date': datetime.strptime(date['start_date'], '%d/%m/%Y').date(),
            'active': True,
        }
        periods = Control_Period.objects.all()
        serializer = ControlPeriodSerializer(data=data)
        if serializer.is_valid():
            if periods is not None:  # TODO REPAIR
                self.check_last_period(request)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotagratListView(APIView):
    def check_last_motagra(self, request):
        last_motagra = Motagrat.objects.last()
        return last_motagra
    def check_available_period(self, request):
        last_period = Control_Period.objects.last()
        if last_period.active and last_period.close_date is None:
            return last_period.id

    # permission_classes = [permissions.IsAuthenticated] #TODO PERMISSION
    def get(self, request, *args, **kwargs):
        motagrat = Motagrat.objects.all()
        serializer = MotagratSerializer(motagrat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        available_period = self.check_available_period(request)
        if available_period is None:
            return Response(
                {"message": "لا يوجد شهر مفتوح لاصافة متاجرة جديدة"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            'name': request.data.get('name'),
            'control_period': available_period
        }
        serializer = MotagratSerializer(data=data)
        if serializer.is_valid():
            print(self.check_last_motagra(request))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotagratProductsListView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        motagrat_products = Motagrat_Products.objects.all()
        serializer = MotagratProductsSerializer(motagrat_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        active_motagra = Motagrat.objects.filter(control_period__active=True).order_by('-control_period_id').first()
        if not active_motagra:
            return Response(
                {"message": "no active motagra"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product = Products.objects.get(name=request.data.get('product'))
        if not product:
            return Response(
                {"message": "product doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        buy_price = float(request.data.get('buy_price'))
        qty = int(request.data.get('qty'))
        pieces = request.data.get('pieces')
        piece_price = request.data.get('piece_price')
        data = {
            'qty': qty,
            "pieces": pieces,
            "piece_price": piece_price,
            "buy_price": buy_price,
            "profit": (int(pieces) * qty * int(piece_price)) - buy_price,
            "product": product.id,
            'motagra': active_motagra.id
        }
        serializer = MotagratProductsSerializer(data=data)
        if serializer.is_valid():
            product.stock += int(request.data.get('qty'))
            product.sell_price = piece_price
            product.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotagraDetailApiView(APIView):
    def get_objects(self, motagra_id):
        try:
            return Motagrat_Products.objects.filter(motagra__id=motagra_id)
        except Products.DoesNotExist:
            return None

    def get(self, request, motagra_id, *args, **kwargs):
        motagrat = self.get_objects(motagra_id=motagra_id)
        total_sell_price = 0
        total_buy_price = 0
        total_profit = 0
        for motagra in motagrat:
            total_sell_price += motagra.total_sell_price_value
            total_buy_price += motagra.buy_price
            total_profit += motagra.profit
        motagrat = self.get_objects(motagra_id=motagra_id)
        if not motagrat:
            return Response(
                {"message": "motagra doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,)
        serializer = MotagraProductsDetailSerializer(motagrat, many=True)
        data = serializer.data
        response = {'data': data, 'total_buy_price': total_buy_price, 'total_sell_price': total_sell_price,
                    'total_profit': total_profit}
        return Response(response, status=status.HTTP_200_OK)


class AvailableProductsApiView(APIView):
    def get(self, request):
        available_products = Products.objects.filter(stock__gt=0)
        if not available_products:
            return Response(
                {"message": "لا يوجد منتجات متاحة حاليا"},
                status=status.HTTP_400_BAD_REQUEST, )
        serializer = AvailableProductsSerializer(available_products, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
