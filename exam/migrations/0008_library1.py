# Generated by Django 3.0.5 on 2022-11-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_remove_video_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=150)),
                ('Subject', models.CharField(max_length=150)),
                ('Date', models.CharField(max_length=150)),
            ],
        ),
    ]