from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name
