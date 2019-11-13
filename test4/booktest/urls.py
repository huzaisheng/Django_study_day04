from django.conf.urls import include,url
from booktest import views

urlpatterns = [
    url(r'^index$', views.index),

    url(r'^temp_var$', views.temp_var), # 模板变量

    url(r'^temp_tags$', views.temp_tags), # 模版标签
    url(r'^temp_filter$', views.temp_filter), #模版过滤器

    url(r'^temp_inherit$', views.temp_inherit), # 模版继承
    url(r'^html_escape$', views.html_escape), # html转义

    url(r'^login$', views.login), # 显示登录页面
    url(r'^login_check$', views.login_check), # 进行登录校验
    url(r'^change_pwd$', views.change_pwd), # 显示修改密码页面
    url(r'^change_pwd_action$', views.change_pwd_action), # 修改密码处理

    url(r'^verify_code$', views.verify_code), # 产生验证码图片
]
