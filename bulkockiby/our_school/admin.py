from django.contrib import admin
from .models import Category, Subcategory, Product, Test, Question, Instruction, User, Work_Name, Cafe
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
import admin_interface.admin


# если нужно опять будет поменять тему что бы в админке открыть нужно admin_interface.admin сделать активным класс  то же самое и для django_summetnote

class CafeAdmin(SummernoteModelAdmin):
    list_display = ('id', 'address')
    list_display_links = ('id', 'address')
    summernote_fields = ('work_schedule')
    prepopulated_fields = {"slug": ("address",)}



class Work_NameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Дополнительная информация',
            {
                'fields': (
                    'cafe',
                    'phone',
                    'telegram',
                    'date_job',
                    'position',
                    'rating',

                )
            }
        )
    )
    list_display = ('id', 'username', 'first_name', 'last_name', 'telegram',  'is_active','date_joined','rating')
    list_display_links = ('id', 'username')
    list_filter = ['rating','is_active']



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'photo')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}

class ProductAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title',  'category', 'subcategoria')
    list_display_links = ('id', 'title')
    summernote_fields = ('recipe')
    prepopulated_fields = {"slug": ("title",)}

class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'test')
    list_display_links = ('id', 'question')

class InstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}







admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Instruction, InstructionAdmin)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Work_Name, Work_NameAdmin)

admin.site.register(Cafe, CafeAdmin)
# Register your models here.

