from instapy import InstaPy
import os
from time import sleep

my_username = os.environ['MY_USERNAME']
my_password = os.environ['MY_PASSWORD']

session = InstaPy(username=my_username, 
                  password=my_password, 
                  headless_browser=True)

# Accept cookies quick and dirty fix.
session.browser.get('https://instagram.com')
session.browser.implicitly_wait(5)
for element in session.browser.find_elements_by_tag_name('button'):
    if element.text.strip().lower() == 'accept all':
        element.click()
        break

sleep(5)

session.login()

session.set_quota_supervisor(enabled=True, peak_comments_daily=240, peak_comments_hourly=21)
session.set_relationship_bounds(enabled=True, max_followers=10000)

session.like_by_tags(["nature", "nature_photography", "polishgirl"], amount=50)
session.set_do_follow(True, percentage=70)
session.set_do_comment(True, percentage=80)
session.set_comments(["Nice!", "Awesome!", "Beautiful :heart_eyes:", "Wow!"])

session.end()
