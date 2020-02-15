# from django.test import LiveServerTestCase  # 自动清理数据库，测试数据
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # luck 访问了首页，不小心提交了一个空信息
        # 输入框中无内容，他就按下了回车键

        # 首页刷新了，显示一个错误的信息
        # 提示代办事项不能为空

        # 他输入一些文字，然后再次提交，这次没问题
        # 他有点调皮，又提交一个空的代办事项

        # 在清单页面他看到一个类似的错误信息
        self.fail('write me!')
