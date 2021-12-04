# -*- coding: utf-8-*-
import scrapy
from scrapy import Request, FormRequest
import json
from PIL import Image
from io import BytesIO
import pytesseract
from scrapy.log import logger


class CaptchaLoginSpider(scrapy.Spider):
    name = "login_captcha"
    start_urls = ["http://XXX.com/"]

    def parse(self, response):
        pass

    # X 网站登录页面的 url(虚构的)
    login_url = "http://XXX.com/login"
    user = "liushuo@XXX.com"
    password = "12345678"

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        # 该方法既是登录页面的解析函数, 又是下载验证码图片的响应处理函数

        # 如果 response.meta['login_response'] 存在, 当前 response 为验证码图片的响应
        # 否则当前 response 为登录页面的响应
        login_response = response.meta.get("login_response")

        if not login_response:
            # Step 1:
            # 此时 response 为登录页面的响应, 从中提取验证码图片的 url, 下载验证码图片
            captchaUrl = response.css(
                "label.field.prepend-icon img::attr(src)"
            ).extract_first()

            captchaUrl = response.urljoin(captchaUrl)

            # 构造 Request 时, 将当前 response 保存到 meta 字典中
            yield Request(
                captchaUrl,
                callback=self.login,
                meta={"login_response": response},
                dont_filter=True,
            )

        else:
            # Step 2:

            # 此时, response 为 验证码 图片 的 响应, response.body 是 图片 二进制 数据
            # login_response 为 登录页面 的 响应, 用其 构造 表单请求 并 发送
            formdata = {
                "email": self.user,
                "pass": self.password,
                "code": self.get_captcha_by_OCR(response.body),
            }

            yield FormRequest.from_response(
                login_response,
                callback=self.parse_login,
                formdata=formdata,
                dont_filter=True,
            )

    def parse_login(self, response):
        info = json.loads(response.text)

        if info["error"] == "0":
            logger.info("登录成功: -)")

            return super().start_requests()

        logger.info("登录失败: -(, 重新登录．..")

        return self.start_requests()

    def get_captcha_by_OCR(self, data):
        img = Image.open(BytesIO(data))
        img = img.convert("L")

        captcha = pytesseract.image_to_string(img)

        img.close()

        return captcha
