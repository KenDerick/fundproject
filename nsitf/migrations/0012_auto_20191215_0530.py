# Generated by Django 2.0.13 on 2019-12-15 04:30

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('nsitf', '0011_csv_upload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employees',
            old_name='middle_name',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='employee_id',
        ),
        migrations.AddField(
            model_name='employees',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='employees',
            name='employer_numb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nsitf.Employers'),
        ),
        migrations.AddField(
            model_name='employees',
            name='other_names',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employees',
            name='phone',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='employees',
            name='profile',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='employers',
            name='branch',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='region', chained_model_field='region', null=True, on_delete=django.db.models.deletion.CASCADE, to='nsitf.Branches'),
        ),
    ]