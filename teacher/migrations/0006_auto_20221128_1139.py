# Generated by Django 3.0.5 on 2022-11-28 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_teacherassignquiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('question_number', models.PositiveIntegerField()),
                ('total_marks', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='teacherassignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Course'),
        ),
        migrations.AlterField(
            model_name='teacherassignquiz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Course'),
        ),
    ]