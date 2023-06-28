# Generated by Django 4.1.3 on 2023-04-14 10:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposite',
            name='created_at',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='created_at',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='created_at',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
    ]
