# Generated by Django 5.0.6 on 2024-05-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_stepeight_stepfive_stepfour_stepseven_stepsix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepfour',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
    ]