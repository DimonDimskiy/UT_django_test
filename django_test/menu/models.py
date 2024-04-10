from django.db import models

# Create your models here.


class Menu(models.Model):
    title = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} of {self.menu}"
