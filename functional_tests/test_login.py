from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from django.core import mail
import re

TEST_EMAIL = "526598423@qq.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):

    def test_can_get_emial_link_to_login(self):
        # 访问网站
        self.browser.get(self.live_server_url)
        # 输入邮箱账号，回车
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn("Check your email", self.browser.find_element_by_tag_name('body').text))

        # 查看邮件，验证关键内容
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body: \n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)

        # 她登录了
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # she want to login out

        self.browser.find_element_by_link_text('Log out').click()

        # she was login out
        self.wait_for(lambda: self.browser.find_element_by_name('email'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)
