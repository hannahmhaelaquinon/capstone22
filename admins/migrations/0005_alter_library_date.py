# Generated by Django 4.1.2 on 2022-12-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0004_alter_library_date_alter_library_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='date',
            field=models.DateField(),
        ),
    ]