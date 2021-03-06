# Generated by Django 2.0.13 on 2019-12-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nsitf', '0005_auto_20191202_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_Approval_manager',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_Entry_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_Sys_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='employers',
            name='Telephone1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employers',
            name='Telephone2',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
