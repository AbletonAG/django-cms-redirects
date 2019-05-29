# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-29 08:26
from __future__ import unicode_literals

import cms.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSRedirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path', models.CharField(db_index=True, help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, verbose_name='redirect from')),
                ('new_path', models.CharField(blank=True, help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200, verbose_name='redirect to')),
                ('response_code', models.CharField(choices=[('301', '301'), ('302', '302')], default='301', help_text='This is the http response code returned if a destination is specified. If no destination is specified the response code will be 410.', max_length=3, verbose_name='response code')),
                ('page', cms.models.fields.PageField(blank=True, help_text='A link to a page has priority over a text link.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Page', verbose_name='page')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'CMS Redirect',
                'verbose_name_plural': 'CMS Redirects',
                'ordering': ('old_path',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='cmsredirect',
            unique_together=set([('site', 'old_path')]),
        ),
    ]
