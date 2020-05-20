from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
# Create your views here.


class RegisterView(View):
    """用户注册"""
    def get(self, request):
        """
        提供注册界面
        :param request:请求对象
        :return:注册界面
        """
        return render(request, 'register.html')


class ImageCodeView(View):
    def get(self, request):
        """
        1.接收前端传递过来的uuid
        2.判断uuid是否获取到
        3.通过调用captcha来生成图片验证码（图片二进制和图片内容）
        4.将图片内容保存到redis中
          uuid作为key，图片内容作为value，同时我们还需要设置一个时效
        5.返回图片二进制给前端
        :param request:
        :return:
        """

        # 1.接收前端传递过来的uuid
        uuid = request.GET.get('uuid')
        # 2.判断uuid是否获取到
        if uuid is None:
            return HttpResponseBadRequest('请求参数错误')
        # 3.通过调用captcha来生成图片验证码（图片二进制和图片内容）
        text, image = captcha.generate_captcha()
        # 4.将图片内容保存到redis中
        redis_conn = get_redis_connection('default')
        # uuid作为key，图片内容作为value，同时我们还需要设置一个时效
        # key设置为 uuid
        # seconds 过期秒数 300秒 5分钟过期时间
        # value text
        redis_conn.setex('img:%s' % uuid, 300, text)
        # 5.返回图片二进制给前端
        return HttpResponse(image, content_type='image/jpeg')

