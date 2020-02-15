# from django.test import LiveServerTestCase  # 自动清理数据库，测试数据
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import  FunctionalTest


MAX_WAIT = 20


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # luck听说有一个非常有趣的在线编辑应用

        # luck访问这个网站
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)  # 设置界面大小

        # 看到输入框完美居中
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # 他注意到了标题和头部都包含了"TO - DO"这个词
        self.assertIn("To-Do", self.browser.title)
        head_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', head_text)

        # 网站邀请他输入一个代办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '请输入一个待办事项！')

        # 他在一个文本框中输入了“ 早上记忆五个英语单词”
        inputbox.send_keys('早上记忆五个英语单词')
        # 他回车确认，页面刷新了数据
        inputbox.send_keys(Keys.ENTER)
        # 显示了它输入要代办的事项
        self.wait_for_row_in_list_table('1、早上记忆五个英语单词')

        inputbox = self.browser.find_element_by_id('id_new_item')  # inputbox.location['x']调用会报错，需要在它之前调用查找方法
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # 页面中又显示了一个代办事项
        # 它继续添加了一条， “中午完成测试app任务”
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('中午完成测试app任务')
        inputbox.send_keys(Keys.ENTER)

        # 回车，页面再次刷新，显示了两项代办事项
        self.wait_for_row_in_list_table('1、早上记忆五个英语单词')
        self.wait_for_row_in_list_table('2、中午完成测试app任务')

        # 它非常高兴，睡觉去了
        # self.fail("finish the test!")

    def test_multiple_users_can_start_lists_at_diffrent_urls(self):
        # jack 创建了新的待办事项
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("确定一个小目标")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1、确定一个小目标')
        # 发现生成了一个唯一的URL
        jack_list_url = self.browser.current_url
        self.assertRegex(jack_list_url, '/lists/.+')

        # 现在，凯莉的新用户访问了该网站
        ## 我们使用了一个新的用户浏览器会话
        ## 确保凯莉的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 凯莉访问了首页
        self.browser.get(self.live_server_url)
        # 页面中看不jack的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('确定一个小目标', page_text)

        # 凯莉添加了一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('凯莉买衣服')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1、凯莉买衣服')

        # 凯莉也获得她唯一的url
        caryly_list_url = self.browser.current_url
        self.assertRegex(caryly_list_url, '/lists/.+')
        self.assertNotEqual(jack_list_url, caryly_list_url)

        # 这个页面还是没有jack的待办清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('确定一个小目标', page_text)
        self.assertIn('凯莉买衣服', page_text)

        # 两人都非常满意，睡觉去了
        self.browser.quit()

