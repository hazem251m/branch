from django.shortcuts import render
from api.models import Motagrat, Motagrat_Products
from .utils import pdf_generation


# Create your views here.

def home(request):
    motagrat = Motagrat.objects.all()
    total_buy_price = 0
    total_sell_price = 0
    total_profit = 0
    context = {
        'motagrat': motagrat,
    }
    if request.method == 'POST':
        selected_motagra = Motagrat.objects.get(id=request.POST.get('selected_option'))
        motagrat_details = Motagrat_Products.objects.filter(motagra=selected_motagra)
        for motagra_details in motagrat_details:
            total_sell_price += motagra_details.sell_price
            total_buy_price += motagra_details.buy_price
            total_profit += motagra_details.profit
        context = {
            'motagrat': motagrat,
            'motagrat_details': motagrat_details,
            'total_buy_price': total_buy_price,
            'total_sell_price': total_sell_price,
            'total_profit': total_profit,
        }
        return pdf_generation(request, context, str(selected_motagra.date))
    return render(request, 'core/home.html', context=context)
