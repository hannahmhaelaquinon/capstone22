# Generated by Django 4.1.2 on 2022-12-14 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_student_bmi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.levels'),
        ),
    ]