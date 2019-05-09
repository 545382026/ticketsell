from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404
from .models import Users, BuyTicket, Tickets
from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from utils.spider_12306 import get_query_list
import datetime
import random
from ticketsell.settings import STATICFILES_DIRS
from ticketsale.forms import UserLoginForm, UserRegisterForm, TicketSearchForm
from ticketsale.serializers import TicketsSerializer
# Create your views here.

# 当前日期更新
def database_update():
    with open(STATICFILES_DIRS[0]+'/update.log', 'r', encoding='utf-8') as f:
        last_update = f.read()
    # 判断上次更新的时间和点击主页当天的时间差,三天更新一次数据
    today = datetime.datetime.now().date()
    temp = datetime.timedelta(days=1)
    if (datetime.datetime.now() - datetime.datetime(int(last_update.split('-')[0]), int(last_update.split("-")[1]), int(last_update.split("-")[2]))).days >3:
        with open(STATICFILES_DIRS[0] + "/update.log", 'w', encoding='utf-8 ') as f:
            f.write(str(today))
        get_query_list(str(today))
        get_query_list(str(today + temp))
        get_query_list(str(today + temp + temp))
    else:
        pass

def init_index_data():
    '''
    用于form与数据库交互
    :return:
    '''

    date_set = list()
    import datetime
    for i in range(0, 7):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        now_year = date.year
        now_month = date.month
        now_day = date.day
        now_date = str(now_year) + "-" + str(now_month) + "-" + str(now_day)
        date_set.append((now_date, now_date))
    return date_set

# 未登陆主页
def index_start(request):

    database_update()
    date_set = init_index_data()
    # 表单
    user_login_form = UserLoginForm()
    user_register_form = UserRegisterForm()
    ticket_search_form = TicketSearchForm()
    ticket_search_form.fields['date_start'].choices = date_set
    tickets = Tickets.objects.all()

    contex = {
        'user_login_form': user_login_form,
        'user_register_form': user_register_form,
        'ticket_search_form': ticket_search_form,
        'ticket': tickets,
    }
    # return HttpResponse('111')
    return render(request, 'index.html', context=contex)

# 登陆后的主页
def index_end(request):
    date_set = init_index_data()
    try:
        name = request.COOKIES['username']
    except Exception as e:
        print(e)
        name = None
    if name == None:
        return index_start(request)
    else:
        ticket_search_form = TicketSearchForm()
        ticket_search_form.fields["date_start"].choices = date_set
        tickets = Tickets.objects.all()
        content = {
            'user_name': name,
            'ticket_search_form': ticket_search_form,
            'tickets': tickets,
        }
        return render(request, 'userhome.html', context=content)

# 注册
def register(request):
    user_form = UserRegisterForm(request.POST)
    if user_form.is_valid():
        if request.method == 'POST':
            register_phone = request.POST['phone']
            if request.POST['password'] == request.POST['again_password']:
                register_password = request.POST['password']
            else:
                rs_str = r'注册失败！密码不一致'
                content = {
                    "string": rs_str
                }
                return render(request, 'register_after.html', context=content)
            register_email = request.POST['email']
            try:
                result = Users.objects.get(phone=register_phone)
            except Exception as e:
                result = None
            # 查询不到该用户，可以注册
            if result is None:
                import datetime
                date = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(
                    datetime.datetime.now().day)
                Users.objects.create(phone=register_phone, password=register_password, email=register_email,
                                     createTime=date)
                rs_str = r'注册成功！'
                content = {
                    "string": rs_str
                }
                return render(request, 'register_after.html', context=content)
            else:
                rs_str = r'用户存在！'
                content = {
                    "string": rs_str
                }
                return render(request, 'register_after.html', context=content)
        else:
            rs_str = r'提交错误，存在不合法数据！'
            content = {
                "string": rs_str
            }
            return render(request, 'register_after.html', context=content)
    else:
        rs_str = r'提交错误，存在不合法数据！'
        content = {
            "string": rs_str
        }
        return render(request, 'register_after.html', context=content)


def login(request):
    user_form = UserLoginForm(request.POST)
    if user_form.is_valid():
        if request.method == 'POST':
            login_phone = request.POST['phone']
            password = request.POST['password']
            try:
                result = Users.objects.get(phone=login_phone, password=password)
            except Exception as e:
                print(e)
                result = None
            if result is None:
                rs_str = r'登陆失败，用户名或者密码错误'
                content = {
                    "string": rs_str,
                    "name": login_phone,
                }
                return render(request, 'register_after.html', context=content)
            else:
                rs_str = r'登录成功！'
                content = {
                    "string": rs_str,
                    "name": login_phone,
                }
                rsp = render(request, 'login_after.html', context=content)
                rsp.set_cookie("username", login_phone)
                return rsp
        else:
            rs_str = r'提交错误，存在不合法数据！'
            content = {
                "string": rs_str,
                "name": ""
            }
            return render(request, 'register_after.html', context=content)
    else:
        rs_str = r'提交错误，存在不合法数据！'
        content = {
            "string": rs_str
        }
        return render(request, 'register_after.html', context=content)


def tickets_search(request):
    if request.method == 'POST':
        start = request.POST['name_start']
        end = request.POST['name_end']
        date = request.POST['date_start']
        print(start, end, date,"***************************")
        tickets = Tickets.objects.filter(name_start=start, name_end=end)
        print(tickets,'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        ticket_list = []
        for item in tickets:
            tic = {'num': item.num, 'name': item.name_start + "-" + item.name_end,
                                                'date_start': item.start_time,"seats": item.seats}
            ticket_list.append(tic)
        content = {
            "tickets": ticket_list,
            "user_phone": "",
        }
        return render(request, "tickets_search.html", context=content)
    else:
        return HttpResponse('不合法查询')

def ticket_buy(request):
    flag = True
    try:
        username = request.COOKIES['username']
    except Exception as e:
        flag = False
    # 没有登录无法买票
    if flag is False:
        content = {
            'result': '非登录用户无法买票，点击按钮返回到主页或回到查询页面'
        }
        return render(request, 'buy_after.html', context=content)
    # 用户登录后
    else:
        if request.method == 'GET':
            ticket_number = request.GET.get('number')
        user = Users.objects.filter(phone=username)
        # 购买车票信息
        buy = user[0].buyticket_set.all()
        # print(buy,'**********',user[0])
        # 判断用户的账号是否已购买
        if buy:
            content = {
                'result': '购票失败，你已经买票了'
            }
            rsp = render(request, 'buy_after_logining.html', context=content)
            return rsp

        else:
            ticket = Tickets.objects.filter(num=ticket_number)
            if ticket[0].seats > 0:
                # print(a,'*******', a.ticket_num)
                # print(ticket[0].num,'*******************',user[0].id)
                a = BuyTicket()
                a.ticket_user_id = Users.objects.get(pk=user[0].id)
                a.ticket_num = ticket[0].num
                a.ticket_name = ticket[0].name_start + "-" + ticket[0].name_end
                a.ticket_seat_num = random.randint(0, ticket[0].seats)
                a.ticket_time = ticket[0].start_time
                a.save()
                Tickets.objects.filter(num=ticket_number).update(seats=ticket[0].seats - 1)
                content = {
                    'result': '购票成功,车次为{}'.format(ticket_number)
                }
                rsp = render(request, 'buy_after_logining.html', context=content)
                return rsp
                # 该车次座位余量为0
            else:

                content = {
                    'result': '购票失败，该车次{}已经没有空余座位了'.format(ticket_number)
                }
                rsp = render(request, 'buy_after_logining.html', context=content)
                return rsp
                # 买过票的情况,那么购票一定是失败的

def order_search(request):
    try:
        username = request.COOKIES['username']
    except:
        username = None
    if username is None:
        pass
    # 用户登录
    else:
        user = Users.objects.filter(phone=username)
        # 用户没有买票
        buy = user[0].buyticket_set.all()
        if buy:
            content = {
                'result': '已经购票',
                'userinfo': buy[0],
                'user': user[0],
            }
        else:
            content = {
                'result': '未购票',
                'userinfo': user[0].buyticket_set.all()
            }

        return render(request, 'order_search.html', context=content)

def order_cancel(request):
    try:
        username = request.COOKIES['username']
    except:
        username = None
    if username is None:
        raise Http404
        # return HttpResponse('有错')
    else:
        user = Users.objects.filter(phone=username)
        buy = user[0].buyticket_set.all()
        if buy:
            now_sets = Tickets.objects.filter(num=buy[0].ticket_num)[0].seats + 1
            Tickets.objects.filter(num=buy[0].ticket_num).update(seats=now_sets)
            user[0].buyticket_set.all().delete()
            content = {
                'string': '退票成功'
            }
        else:
            content = {
                'string': '取消失败，您未定票'
            }

        return render(request, 'cancel_after.html', context=content)


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(renderer_classes=[renderers.JSONRenderer])
    def highlight(self, request, *args, **kwargs):
        ticket = self.get_object()
        return Response(ticket.highlighted)