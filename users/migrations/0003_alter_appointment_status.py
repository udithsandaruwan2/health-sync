# Generated by Django 5.1.1 on 2024-10-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_loyaltypoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Cancelled'), (4, 'Reviewed')], default=1),
        ),
    ]