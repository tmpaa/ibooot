from instapy import InstaPy
import os
from time import sleep
import signal
import threading
import datetime
import random

current_datetime = datetime.datetime.now(datetime.timezone.utc)
test_flag = False

if test_flag or (current_datetime.hour >= 9 and current_datetime.hour <= 14):
    if test_flag == False:
        sleep_time = random.randint(1800, 3600) # sleep randomly for 30 minutes to 1 hour
        print(f"Insta bot is sleeping for: {sleep_time}")
        sleep(sleep_time)

    # ------------ Break execution of the program - separate Thread ------------------

    class ExitCommand(Exception):
        pass

    def signal_handler(signal, frame):
        raise ExitCommand()

    def break_program_thread(afterTime):
        stop_time = datetime.datetime.now() + datetime.timedelta(minutes=afterTime)
        while datetime.datetime.now() <= stop_time:
            pass
        os.kill(os.getpid(), signal.SIGUSR1)

    signal.signal(signal.SIGUSR1, signal_handler)

    # --------------- Insta bot -------------------
    print(f"Insta bot starts at: {datetime.datetime.now(datetime.timezone.utc)}")

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
    session.set_relationship_bounds(enabled=True, delimit_by_numbers=True, max_followers=10000)

    #session.set_do_follow(True, percentage=70)
    session.set_do_comment(True, percentage=80)
    session.set_comments(["Nice!", "Awesome!", "Beautiful :heart_eyes:", "Wow!"])
    
    threading.Thread(target=break_program_thread, args=[60 // random.randint(2, 3)]).start()
    session.like_by_tags(["nature", "nature_photography", "polishgirl"], amount=35)

    session.end()
