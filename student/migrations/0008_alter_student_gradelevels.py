# Generated by Django 4.0.2 on 2022-12-05 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_student_gradelevels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gradelevels',
            field=models.TextField(blank=True, choices=[('Grade 2', 'Grade 2'), ('Grade 4', 'Grade 4'), ('Grade 6', 'Grade 6'), ('Kindergarten', 'Kindergarten'), ('Grade 5', 'Grade 5'), ('Grade 3', 'Grade 3'), ('Grade 1', 'Grade 1')], max_length=20),
        ),
    ]