# Generated by Django 3.1.1 on 2020-09-03 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_cartitem_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(default="test", max_length=15),
            preserve_default=False,
        ),
    ]