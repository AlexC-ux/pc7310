from django.db import models

class Contacts(models.Model):
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["-phone"]

    def __str__(self):
        return f"{self.phone}"

class TestTexts(models.Model):
    page_name = models.CharField(max_length=200)
    html_content = models.TextField()
    class Meta:
        verbose_name = "Контент страниц"
        verbose_name_plural = "Контент страниц"
        ordering = ["-page_name"]

    def __str__(self):
        return f"{self.page_name}"