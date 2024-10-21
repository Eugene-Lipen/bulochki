import datetime

from django.db import models
from django.urls import reverse
from our_school.models import User
from PIL import Image
class TestingCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название теста", unique=True)
    slug = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Название теста'
        verbose_name_plural = 'Название тестов'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('testing', kwargs={'slug_category_test': self.slug})


class Question(models.Model):
    testing_category = models.ForeignKey(TestingCategory, on_delete=models.CASCADE, verbose_name='Тест')
    text = models.CharField(verbose_name='Вопрос', max_length=250)
    img = models.ImageField(upload_to='photos/test_img/', blank=True, verbose_name='Картинка')
    num_right = models.IntegerField(verbose_name='Кол-во правильных ответов')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.__dict__)
        path=self.img

        if path == '':
            pass
        else:
            image = Image.open(self.img.path)


            if image.height > 50 or image.width > 50:
                new_img = (320, 480)
                image.thumbnail(new_img)
                image.save(self.img.path)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.CharField(verbose_name='Ответ', max_length=250)
    right = models.BooleanField(verbose_name='Правильный', default=False)

    def __str__(self):
        return self.text

class TestingPeople(models.Model):
    people = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Сотрудник')
    test = models.ForeignKey(TestingCategory, on_delete=models.CASCADE, verbose_name='Тест')
    att = models.BooleanField(verbose_name='Оценка', default=False)
    date_job = models.DateField(default=datetime.date.today(), verbose_name="Дата начала теста")
    date_stop = models.DateField(default=datetime.date.today() + datetime.timedelta(days=14), verbose_name="Дата окончания теста")
    attempt = models.IntegerField(default=0)
    col = models.IntegerField(default=2)


    class Meta:
        verbose_name = 'Тестируемый'
        verbose_name_plural = 'Тестируемые'
    def __str__(self):
        return str(self.people)



class AnswerPeople(models.Model):
    test = models.CharField(max_length=250, verbose_name='Название теста')
    people = models.CharField(max_length=250,verbose_name='Сотрудник')
    document = models.FileField(upload_to='answer_text/', verbose_name='Тест')

    class Meta:
        verbose_name = 'Тест сотрудника'
        verbose_name_plural = 'Тесты сотрудников'
    def __str__(self):
        return str(self.people)
