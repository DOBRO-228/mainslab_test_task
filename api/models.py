from django.db import models


class Client(models.Model):
    name = models.TextField(unique=True)


class Organization(models.Model):
    name = models.TextField()
    client = models.ForeignKey(
        Client,
        related_name='organizations',
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ('name', 'client')


class Bill(models.Model):
    organization = models.ForeignKey(
        Organization,
        related_name='bills',
        on_delete=models.PROTECT,
    )
    number = models.IntegerField()
    sum = models.IntegerField()
    date = models.DateField()

    class Meta:
        unique_together = ('organization', 'number')
