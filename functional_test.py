from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		# 退出网站，睡觉去了
		self.browser.quit()
	
	def test_a_list(self):
		#luck听说有一个非常有趣的在线编辑应用

		# luck访问这个网站
		self.browser.get('http://localhost:8000')

		# 他注意到了标题和头部都包含了"TO - DO"这个词
		self.assertIn("To-Do", self.browser.title)
		slef.fail("finish the test!")
		
		# 网站邀请他输入一个代办事项

		# 他在一个文本框中输入了“ 早上记忆五个单词”

		# 他回车确认，页面刷新了数据

		# 显示了它输入要代办的事项

		# 页面中又显示了一个代办事项

		# 它继续添加了一条， “中午完成测试app任务”

		# 回车，页面再次刷新，显示了两项代办事项

		# 它很满意，页面记住了它的事项

if __name__ == "__main__":
	unittest.main(warnings='ignore')