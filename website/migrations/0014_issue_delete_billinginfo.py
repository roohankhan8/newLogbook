# Generated by Django 5.0.6 on 2024-05-31 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_research_remove_stepthree_research'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('teamId', models.IntegerField()),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('expert_name', models.CharField(max_length=255)),
                ('expert_credentials', models.CharField(max_length=255)),
                ('problem_identified', models.TextField(blank=True, null=True)),
                ('problem_faced', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='BillingInfo',
        ),
    ]