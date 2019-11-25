from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        # 退出网站，睡觉去了
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_to_do_list(self):
        #luck听说有一个非常有趣的在线编辑应用

        # luck访问这个网站
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        # 显示了它输入要代办的事项
        self.check_for_row_in_list_table('1、早上记忆五个英语单词')


        # 页面中又显示了一个代办事项
        # 它继续添加了一条， “中午完成测试app任务”
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('2、中午完成测试app任务')
        
        # 回车，页面再次刷新，显示了两项代办事项
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('2、中午完成测试app任务')
            

        # 它很满意，页面记住了它的事项
        self.fail("finish the test!")

if __name__ == "__main__":
    unittest.main(warnings='ignore')
