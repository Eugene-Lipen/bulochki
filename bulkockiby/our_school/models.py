import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image




class Cafe(models.Model):
    address = models.CharField(max_length=250, verbose_name="Адрес")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    phone = PhoneNumberField(blank=True, verbose_name="Телефонный номер")
    work_schedule = models.TextField(verbose_name='График работы', blank=True, null=True)
    long = models.CharField(max_length=250, verbose_name="Широта")
    lat = models.CharField(max_length=250, verbose_name='Долгота')

    class Meta:
        verbose_name = 'Кафе'
        verbose_name_plural = 'Кафе'

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('cafe', kwargs={'address_slug': self.slug})

# пользователи админы и личные кабинеты

class Work_Name(models.Model):
    name = models.CharField(max_length=100, verbose_name="Должность")

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class User(AbstractUser):

    CURRENCY_CHOICES = [
        ('1',1),
        ('2',2),
        ('3',3),
        ('4',4),
        ('5',5),
    ]
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, verbose_name='Кафе', null=True)
    phone = PhoneNumberField(blank=True, verbose_name="Телефонный номер")
    date_job = models.DateField(default=datetime.date.today(), verbose_name="Дата устройства на работу")
    telegram = models.CharField(max_length=255, blank=True)
    position = models.ForeignKey(Work_Name,  on_delete=models.CASCADE, blank=True, null=True, verbose_name='Должность')
    rating = models.CharField(max_length=1, choices=CURRENCY_CHOICES, default=1, verbose_name='Рейтинг')


    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username




# отображение категорий подкатегорий лекций и содержание в обучающем блоке
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Категория", unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/category', null=True, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 50 or img.width > 50:
            new_img = (320, 240)
            img.thumbnail(new_img)
            img.save(self.photo.path)


    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

class Subcategory(models.Model):
    title = models.CharField(max_length=200, verbose_name="Подкатегория", unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/subcategoria/', null=True, verbose_name='Картинка')
    category = models.ForeignKey(Category,  on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 50 or img.width > 50:
            new_img = (320, 240)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    def get_absolute_url(self):
        cat_id = Category.objects.filter(title=self.category).values()
        return reverse('subcategory', kwargs={'category_slug': cat_id[0]['slug'], 'subcategory_slug': self.slug})

class Product(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    subcategoria = models.ForeignKey(Subcategory, on_delete= models.CASCADE, verbose_name="Подкатегория")
    recipe = models.TextField(verbose_name='Рецепт', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/product/', verbose_name='Фото')
    video = models.FileField(upload_to='video/', blank=True, null=True, verbose_name='Видео')


    class Meta:
        verbose_name = 'Подробнее'
        verbose_name_plural = 'Подробнее'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 50 or img.width > 50:
            new_img = (320, 240)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    def get_absolute_url(self):
        cat_id = Category.objects.filter(title=self.category).values()
        subcat_id = Subcategory.objects.filter(title=self.subcategoria).values()
        return reverse('product', kwargs={'category_slug': cat_id[0]['slug'], 'subcategory_slug': subcat_id[0]['slug'], 'product_slug': self.slug})


class Instruction(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, verbose_name='Название')
    slug = models.CharField(max_length=255,unique=True)
    document = models.FileField(upload_to='document/', verbose_name='Документ')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('instruction', kwargs={'slug_instruction': self.slug})

# блок тестов и вопросаов
class Test(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test', kwargs={'test': self.slug})

class Question(models.Model):
    question = models.TextField(null=True)
    answer = models.CharField(max_length=255)
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    right_one = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    
