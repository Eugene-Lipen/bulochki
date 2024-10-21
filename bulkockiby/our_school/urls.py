from django.urls import path, include
from .views import show_category, show_subcategory, show_product, show_card, show_test, entry, account_logout, instructions, pdf_view, show_account, SearchResultsView, cafes, cafe

urlpatterns = [
    path('', entry, name='entry'),
    path('testing/<slug:slug_category_test>/', include('testing.urls'), name='testing'),
    path('logout/', account_logout, name='account_logout'),
    path('account/', show_account, name='account'),
    path('category/', show_category,name='top'),
    path('category/<slug:category_slug>/', show_subcategory, name='category'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', show_product, name='subcategory'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>', show_card, name='product'),
    path('test/', show_test, name='test'),
    path('instructions/', instructions, name='instructions'),
    path('instructions/<slug:slug_instruction>', pdf_view, name='instruction'),
    path('cafes/', cafes, name='cafes'),
    path('cafes/<slug:address_slug>', cafe, name='cafe'),


    path('search/', SearchResultsView.as_view(), name='search_results'),
    #path(r'^view-pdf/$', pdf_view, name='pdf_view'),

]
