# Generated by Django 3.1.1 on 2020-09-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_auto_20200902_1720"),
    ]

    operations = [
        migrations.AddField(
            model_name="productimage",
            name="name",
            field=models.CharField(default="test", max_length=30),
            preserve_default=False,
        ),
    ]