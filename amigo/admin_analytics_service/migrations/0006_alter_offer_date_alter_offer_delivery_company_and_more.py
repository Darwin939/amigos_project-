# Generated by Django 4.0.2 on 2022-02-18 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_analytics_service', '0005_order_cancel_reason_order_fail_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='delivery_Company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_analytics_service.delivery_company'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offeredPriceTenge',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='admin_analytics_service.order'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='type',
            field=models.CharField(blank=True, choices=[('OfferEvent', 'OfferEvent'), ('OfferAcceptEvent', 'OfferAcceptEvent')], max_length=255, null=True),
        ),
    ]