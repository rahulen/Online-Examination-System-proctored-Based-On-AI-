# Generated by Django 3.2.20 on 2024-05-03 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='material_file',
            field=models.FileField(blank=True, null=True, upload_to='study_material\\'),
        ),
    ]
