from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django_admin_json_editor import JSONEditorWidget
from import_export import resources
from import_export.admin import ExportMixin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


# Schema for json field in products. For json editor.
DATA_SCHEMA = {
    'type': 'object',
    'title': 'Data',
    'properties': {
    },
}

class JSONModelAdminForm(forms.ModelForm):
    """ Class form for json editor """
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'characteristics': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
        }

class ProductResource(resources.ModelResource):

    class Meta:
        model = Product

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Registers Category model to admin """

    list_display = ['category_name', 'category_slug']
    prepopulated_fields = {'category_slug': ('category_name', )}

@admin.register(Product)
class ProductAdmin(ExportMixin, SimpleHistoryAdmin):
    """ Registers Product model to admin """

    list_display = ['product_name', 'category_link', 'product_slug', 'product_price', 'product_is_aviable', 'product_created', 'product_updated', 'product_image']
    list_filter = ['product_category', 'product_is_aviable', 'product_created', 'product_updated']
    list_editable = ['product_price', 'product_is_aviable']
    prepopulated_fields = {'product_slug': ('product_name',)}
    form = JSONModelAdminForm
    search_fields = ['product_name', 'product_description']
    inlines = [ProductStockInline]
    date_hierarchy = 'product_created'
    resource_class = ProductResource

    @admin.display(description='Category')
    def category_link(self, obj):
        url = reverse('admin:webshop_category_change', args=[obj.product_category.pk])
        return format_html('<a href="{}">{}</a>', url, obj.product_category.category_name)

    category_link.short_description = 'Category'


@admin.register(ProductReview)
class ReviewAdmin(admin.ModelAdmin):
    """ Registers Review model to admin """

    list_display = ['product', 'author', 'date_published']
    list_filter = ['product', 'date_published']

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    """ Registers UserInfo model to admin """

    list_display = ['user', 'purchased_items']


class ProductStockForm(forms.ModelForm):
    """ Custom form for ProductStock """
    class Meta:
        model = ProductStock
        fields = '__all__'


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    pass
    


class ProductForm(forms.ModelForm):
    stocks = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Stocks', is_stacked=False),
        required=False,
        label='Stocks'
    )

    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['stock_name', 'stock_slug']
    inlines = [ProductStockInline]
    list_filter = ['products']
    form = ProductForm
    filter_horizontal = ('products',)
    readonly_fields = ('get_stock_names',)
    prepopulated_fields = {'stock_slug': ('stock_name',)}
    raw_id_fields = ('products',)  # Добавлен фильтр raw_id_fields

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "products":
            kwargs["queryset"] = Product.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        products = form.cleaned_data.get('products')
        if products is not None:
            for product in products:
                ProductStock.objects.update_or_create(
                    stock=obj,
                    product=product,
                )

    def get_stock_names(self, obj):
        return ', '.join([str(product) for product in obj.products.all()])
    get_stock_names.short_description = 'Products'




    