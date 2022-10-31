# Generated by Django 4.0.4 on 2022-10-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default=False, null=True, upload_to='category', verbose_name='Category Image'),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default=False, max_length=150),
        ),
    ]
