# Generated by Django 4.0.2 on 2022-02-18 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_analytics_service', '0006_alter_offer_date_alter_offer_delivery_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='delivery_company',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='admin_analytics_service.delivery_company'),
        ),
    ]
