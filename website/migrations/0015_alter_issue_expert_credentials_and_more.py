# Generated by Django 5.0.6 on 2024-05-31 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_issue_delete_billinginfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='expert_credentials',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='expert_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]