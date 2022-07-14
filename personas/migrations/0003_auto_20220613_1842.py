# Generated by Django 3.1.1 on 2022-06-13 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_auto_20220613_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.CharField(max_length=100, unique=True, verbose_name='Correo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre'),
        ),
    ]