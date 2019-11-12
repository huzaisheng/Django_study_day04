from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from booktest.models import BookInfo
# Create your views here.


# def my_render(request, template_path, context={}):
#     # 1.加载模版文件，获取一个模版对象
#     temp = loader.get_template(template_path)
#     # 2.定义模版上下文，给模版文件传数据
#     # context = {}
#     # 3.模版渲染，产生一个替换后的html内容
#     res_html = temp.render(context)
#     # 4.返回应答
#     return HttpResponse(res_html)


def login_required(view_func):
    """登录判断装饰器"""
    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录，跳转到登录页
            return redirect('/login')
    return wrapper

# /index
def index(request):
    # return my_render(request, 'booktest/index.html')
    # Django提供的render方法，返回一个HttpResponse类的对象
    return render(request,'booktest/index.html')

def temp_var(request):
    """模版变量"""
    my_dict = {'title':'字典键值'}
    my_list = [1,2,3]
    book = BookInfo.objects.get(id=1)
    context = {'my_dict':my_dict,'my_list':my_list,'book':book}
    return render(request, 'booktest/temp_var.html',context)

# /temp_tags
def temp_tags(request):
    """模型标签"""
    # 1。查找所有图书的信息
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_tags.html',{'books':books})

# /temp_filter
def temp_filter(request):
    """模型标签"""
    # 1。查找所有图书的信息
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_filter.html',{'books':books})

# /temp_inherit
def temp_inherit(request):
    """模版继承"""
    return render(request, 'booktest/child1.html')


def html_escape(request):
    """html转义"""
    return render(request, 'booktest/html_escape.html',{'content':'<h1>hello</h1>'})


def login(requset):
    """显示登录页面"""
    # 判断用户是否登录
    if requset.session.has_key('islogin'):
        # 用户已登录，跳转到修改密码页面
        return redirect('/change_pwd')
    else:
        # 用户未登录
        # 获取cookie username
        if 'username' in requset.COOKIES:
            # 获取记住的用户名
            username = requset.COOKIES['username']
        else:
            username = ''
        return render(requset, 'booktest/login.html',{'username':username})

def login_check(request):
    # request.POST 保存的是post方式提交的参数
    # request.GET 保存的是get方式提交的参数
    # 1、获取提交的用户名和密码
    # print(type(request.POST)) # 返回的是QueryDict对象
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    # 获取用户输入的验证码
    vcode1 = request.POST.get('vcode')
    # 获取session中保存的验证码
    vcode2 = request.session.get('verifycode')

    if vcode1 != vcode2:
        return redirect('/login')
    # 2、进行登录的校验
    # 实际开发：根据用户名和密码查找数据库
    # 模拟: smart  123
    if username == 'smart' and password == '123':
        # 用户名密码正确，跳转到修改密码页面
        response = redirect('/change_pwd')
       # 判断是否需要记住用户名
        if remember == 'on':
            # 设置cookie username的过期时间为1周
            response.set_cookie('username', username, max_age=7*24*3600)
            # response.set_cookie('password',password, max_age=7*24*3600)
        # 记住用户登录状态
        # 只要session中有islogin，就认为用户已登录
        request.session['islogin'] = True
        # 记住登录的用户名
        request.session['username'] = username
        return response
    else:
        return redirect('/login')

# /change_pwd
@login_required
def change_pwd(request):
    """显示密码修改页面"""
    return render(request, 'booktest/change_pwd.html')

@login_required
def change_pwd_action(request):
    """模拟修改密码处理"""
    # 1、获取新密码
    pwd = request.POST.get('pwd')
    # 获取用户名
    username = request.session.get('username')
    # 2、实际开发的时候：修改对用数据库中的内容
    # 3、返回一个应答
    return HttpResponse('%s 修改密码为：%s' %(username,pwd))


from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO

# /verify_code
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('calibri.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')