from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import product_page, CategoryViewSet, ProductViewSet, ProductStockViewSet, StockViewSet, \
    ProductReviewViewSet, UserInfoViewSet

app_name = 'webshop'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'productstocks', ProductStockViewSet, basename='productstock')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'reviews', ProductReviewViewSet, basename='productreview')
router.register(r'userinfos', UserInfoViewSet, basename='userinfo')

urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    path('api/', include(router.urls)),
    path('', views.MainPage.as_view(), name='shop_page'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('remove_review/', views.remove_review, name='remove_review'),
    path('buy/', views.buy_product, name='buy_product'),    
    path('filter/', views.ProductFilter.as_view(), name='filter'),
    path('shop/', views.ShopPage.as_view(), name='shop_page'),
    path('shop/<category_slug>', views.CategoryPage.as_view() , name='category_page'),
    path('shop/<category_slug>/<product_slug>', views.ProductPage.as_view(), name='product_page'),
    path('profile/<username>', views.UserProfile.as_view(), name='profile'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_page, name='product_page'),
]
