# Generated by Django 3.1.1 on 2020-10-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20201001_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='task',
            field=models.IntegerField(),
        ),
    ]
