# Generated by Django 5.0.6 on 2024-06-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_delete_inventor'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='problem',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
