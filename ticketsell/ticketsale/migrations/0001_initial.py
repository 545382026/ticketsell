# Generated by Django 2.2 on 2019-05-08 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50, verbose_name='车票日期')),
                ('num', models.CharField(max_length=210, verbose_name='车票编号')),
                ('name_start', models.CharField(max_length=30, verbose_name='始发站')),
                ('name_end', models.CharField(max_length=30, verbose_name='终点站')),
                ('start_time', models.CharField(max_length=50, verbose_name='发车时间')),
                ('end_time', models.CharField(max_length=50, verbose_name='到达时间')),
                ('seats', models.IntegerField(default=200, verbose_name='剩余座位')),
            ],
            options={
                'verbose_name': '车票信息',
                'verbose_name_plural': '车票信息',
                'db_table': 'Tickets',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, verbose_name='用户手机号')),
                ('password', models.CharField(max_length=20, verbose_name='账户密码')),
                ('name', models.CharField(max_length=20, null=True, verbose_name='用户姓名')),
                ('name_id', models.IntegerField(max_length=20, null=True, verbose_name='用户身份证')),
                ('createTime', models.DateTimeField(verbose_name='账户创建时间')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='账户关联邮箱')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'Users',
            },
        ),
        migrations.CreateModel(
            name='BuyTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_num', models.CharField(max_length=10, null=True, verbose_name='购买车票编号')),
                ('createTime', models.DateField(null=True, verbose_name='购买车票日期')),
                ('ticket_seat_num', models.IntegerField(max_length=20, null=True, verbose_name='购买车票座位号')),
                ('ticket_time', models.DateTimeField(max_length=50, null=True, verbose_name='购买车票发车时间')),
                ('ticket_user_id', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketsale.Users', verbose_name='用户关联')),
            ],
            options={
                'verbose_name': '购买车票信息',
                'verbose_name_plural': '购买车票信息',
                'db_table': 'BuyTicket',
            },
        ),
    ]