# Generated by Django 2.0.13 on 2019-12-08 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nsitf', '0008_auto_20191206_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reg_Task_Queue',
            fields=[
                ('code', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reg_Task_Route',
            fields=[
                ('branch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nsitf.Branches')),
                ('approval_queue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approvalqueue', to='nsitf.Reg_Task_Queue')),
            ],
        ),
        migrations.CreateModel(
            name='Reg_Tasks',
            fields=[
                ('code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nsitf.Employers')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('CAC_no', models.IntegerField(blank=True, null=True)),
                ('CAC_reg_date', models.DateField(blank=True, null=True)),
                ('sent_on', models.DateTimeField(blank=True, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taskbranch', to='nsitf.Branches')),
                ('queue_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_queue', to='nsitf.Reg_Task_Queue')),
                ('sent_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nsitf.Registration_Status')),
            ],
        ),
    ]
