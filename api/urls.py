from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListApiView.as_view(), name='products'),
    path('product/<int:product_id>', views.ProductDetailApiView.as_view(), name='product_detail'),
    path('available_products/', views.AvailableProductsApiView.as_view(), name='available_products'),
    path('control_periods/', views.ControlPeriodListView.as_view(), name='periods'),
    path('motagrat/', views.MotagratListView.as_view(), name='motagrat'),
    path('motagrat_products/', views.MotagratProductsListView.as_view(), name='motagrat_products'),
    path('motagra_details/<int:motagra_id>', views.MotagraDetailApiView.as_view(), name='motagra_details'),

]
