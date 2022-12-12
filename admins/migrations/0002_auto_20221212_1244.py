# Generated by Django 3.0.5 on 2022-12-12 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admins.Levels'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Result',
        ),
    ]
