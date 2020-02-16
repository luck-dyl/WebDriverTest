# from django.test import LiveServerTestCase  # 自动清理数据库，测试数据
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # luck 访问了首页，不小心提交了一个空信息
        # 输入框中无内容，他就按下了回车键
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # 首页刷新了，显示一个错误的信息
        # 提示代办事项不能为空
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        )
                      )

        # 他输入一些文字，然后再次提交，这次没问题
        self.browser.find_element_by_id('id_new_item').send_keys('jack 被确诊冠状病毒')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1、jack 被确诊冠状病毒')
        # 他有点调皮，又提交一个空的代办事项
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # 在清单页面他看到一个类似的错误信息
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You can not have an empty list item'
        )
                      )

        # 输入文字之后就没有问题
        self.browser.find_element_by_id('id_new_item').send_keys('武汉封城了')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1、jack 被确诊冠状病毒')
        self.wait_for_row_in_list_table('2、武汉封城了')

