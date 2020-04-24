from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from django.core import mail
import re, os, poplib, time

# TEST_EMAIL = "3479566308@qq.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(subject, email.subject)
            return email.body

        email_id = None
        start_time = time.time()
        inbox = poplib.POP3_SSL('pop.qq.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['QQ_PASSWORD'])
            while time.time() - start_time < 60:
                # get last ten email
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf-8') for l in lines]
                    print(lines)
                    if f'Subject:{ellipsis}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_emial_link_to_login(self):

        # 访问网站
        if self.staging_server:
            test_email = '3479566308@qq.com'
        else:
            test_email = 'edith@example.com'
        self.browser.get(self.live_server_url)

        # 输入邮箱账号，回车
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn("Check your email", self.browser.find_element_by_tag_name('body').text))

        # 查看邮件，验证关键内容
        body = self.wait_for_email(test_email, SUBJECT)
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body: \n{body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)

        # 她登录了
        self.wait_to_be_logged_in(email=test_email)

        # she want to login out

        self.browser.find_element_by_link_text('Log out').click()

        # she was login out
        self.wait_for(lambda: self.browser.find_element_by_name('email'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(test_email, navbar.text)
