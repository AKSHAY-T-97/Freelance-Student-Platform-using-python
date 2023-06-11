# Generated by Django 4.1.5 on 2023-05-01 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=255)),
                ('course', models.CharField(max_length=255)),
                ('university', models.CharField(max_length=255)),
                ('uploaded_file', models.FileField(upload_to='uploaded_documents/')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('address', models.TextField()),
                ('gender', models.CharField(max_length=10)),
                ('course', models.CharField(max_length=100)),
                ('college', models.CharField(max_length=100)),
                ('type_student_rec', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews_college',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=200)),
                ('board', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
                ('review', models.TextField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]