# Generated by Django 2.2 on 2019-05-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketsale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyticket',
            name='ticket_name',
            field=models.CharField(max_length=20, null=True, verbose_name='购买车票起始站点'),
        ),
        migrations.AlterField(
            model_name='buyticket',
            name='createTime',
            field=models.DateTimeField(null=True, verbose_name='购买车票日期'),
        ),
        migrations.AlterField(
            model_name='buyticket',
            name='ticket_seat_num',
            field=models.IntegerField(null=True, verbose_name='购买车票座位号'),
        ),
        migrations.AlterField(
            model_name='buyticket',
            name='ticket_time',
            field=models.CharField(max_length=50, null=True, verbose_name='购买车票发车时间'),
        ),
        migrations.AlterField(
            model_name='users',
            name='name_id',
            field=models.IntegerField(null=True, verbose_name='用户身份证'),
        ),
    ]