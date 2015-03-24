# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptanceCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('criteria', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('comment_location', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField()),
                ('sign_off_type', models.CharField(choices=[('Matr', 'Material'), ('Cond', 'Conditional'), ('Good', 'Good to have'), ('Comp', 'Compliant')], max_length=15)),
                ('actions_to_close', models.TextField(null=True, blank=True)),
                ('action_comments', models.TextField(null=True, blank=True)),
                ('date_closed', models.DateTimeField(blank=True, null=True, verbose_name='Date Comment Closed')),
                ('acceptance_critieria', models.ForeignKey(blank=True, to='qareviewer.AcceptanceCriteria', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_first_issued', models.DateField(blank=True, null=True, verbose_name='Date First Issued')),
                ('date_signed_off', models.DateField(blank=True, null=True, verbose_name='Date Signed Off')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewIteration',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=30)),
                ('iteration_number', models.BigIntegerField(verbose_name='Iteration No.')),
                ('publisher', models.CharField(max_length=40)),
                ('issued_date', models.DateTimeField(verbose_name='Date Issued')),
                ('reviewer', models.CharField(max_length=40)),
                ('review_date', models.DateTimeField(verbose_name='Date Reviewed')),
                ('deliverable', models.ForeignKey(to='qareviewer.Deliverable')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateDeliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('activity', models.ForeignKey(blank=True, to='qareviewer.Activity', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateDeliverableSection',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('purpose', models.TextField()),
                ('template_deliverable', models.ForeignKey(blank=True, to='qareviewer.TemplateDeliverable', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deliverable',
            name='template_deliverable',
            field=models.ForeignKey(to='qareviewer.TemplateDeliverable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliverable',
            name='theme',
            field=models.ForeignKey(to='qareviewer.Theme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='iteration_comment_closed',
            field=models.ForeignKey(blank=True, to='qareviewer.ReviewIteration', related_name='iteration_comment_closed', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='review_iteration',
            field=models.ForeignKey(related_name='review_iteration', to='qareviewer.ReviewIteration'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='template_deliverable_section',
            field=models.ForeignKey(blank=True, to='qareviewer.TemplateDeliverableSection', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acceptancecriteria',
            name='deliverable_section',
            field=models.ForeignKey(to='qareviewer.TemplateDeliverableSection'),
            preserve_default=True,
        ),
    ]
