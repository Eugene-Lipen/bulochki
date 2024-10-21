from django.contrib import admin
from .models import Answer,Question, TestingCategory, TestingPeople, AnswerPeople

class AnswerPeopleAdmin(admin.ModelAdmin):
    list_display = ('id', 'people', 'test', 'document')
    list_display_links = ('id', 'people', 'test', 'document')
    list_filter = ['test', 'people']



class TestingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}



class AnswersInLine(admin.TabularInline):
    model = Answer
    extra = 4
    list_filter = ['testing_category_id']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id','text')
    list_display_links = ('id','text')

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInLine]
    list_display = ('testing_category', 'text')
    list_display_links = ('testing_category', 'text')
    #list_filter = ['text','testing_category_id']

class TestingPeopleAdmin(admin.ModelAdmin):
    list_display = ('test', 'people', 'att')
    list_display_links = ('test', 'people',)
    list_filter = ['test', 'people','att']
    exclude = ('col', 'attempt','att')


admin.site.register(AnswerPeople,AnswerPeopleAdmin)
admin.site.register(TestingPeople, TestingPeopleAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Answer, AnswerAdmin)
admin.site.register(TestingCategory,TestingCategoryAdmin)


