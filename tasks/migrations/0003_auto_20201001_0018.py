# Generated by Django 3.1.1 on 2020-09-30 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20200930_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completion_date',
            field=models.DateField(null=True),
        ),
    ]