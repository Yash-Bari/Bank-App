# Generated by Django 5.0.6 on 2024-07-04 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_alter_user_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InsuranceProduct',
        ),
    ]
