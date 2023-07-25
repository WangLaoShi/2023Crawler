# //span[@class="position-head-wrap-name"]/span[1] 标题
# //dd[@class="job-advantage"]/span 职位诱惑四字
# //dd[@class="job_bt"]/h3 职位描述
# //span[@class="position-head-wrap-name"]/span[2] 薪资
# //dd[@class="label-wrapper"]/h3 附加信息
# //dd[@class="job-address clearfix"]/h3 工作地址
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions, DesiredCapabilities
from selenium.webdriver.common.by import By
from urllib import parse
from SQLiteHelper import *
import csv
from selenium.common.exceptions import NoSuchElementException


options = ChromeOptions()

options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
driver = Chrome(executable_path='chromedriver', options=options)

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def get_joblist_urls(keyword, city):
    driver.get("https://www.lagou.com/jobs/list_" + parse.quote(keyword) + "?city=" + parse.quote(city))
    urls = []
    tempVar = ''
    times = 0  # 定位不到的尝试次数
    while True:
        try:
            urlsInOnePage = [i.get_attribute('href') for i in WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     '//div[@class="s_position_list "]/ul[@class="item_con_list"]//a[@class="position_link"]')))]
            print(keyword + ' ' + city + "获取到 ", len(urlsInOnePage), " 个连接")
        except:
            time.sleep(2 * random.randint(1, 5))
            print("定位不到--->继续", times, " 次尝试，超过 10 次，将跳出")
            times += 1
            continue
        if times > 10:
            break
        print(urlsInOnePage)
        # 如果已经到了最后一页了，直接返回
        if check_exists_by_xpath('//span[@class="pager_next pager_next_disabled"]'):
            print("到最后一页，不能翻页了")
            return urls
        if urlsInOnePage[0] != tempVar:
            urls.extend(urlsInOnePage)
            tempVar = urlsInOnePage[0]
            now = time.time()
            while time.time() - now < 5:
                try:
                    driver.find_element(By.XPATH, '//span[@class="pager_next "]').click()
                    sleep_time = 1 * random.randint(1, 5)
                    print(sleep_time, " 秒后，点下一页")
                    time.sleep(sleep_time)
                    break
                except Exception as ex:
                    driver.refresh()
                    print(ex)
                    pass
            else:
                return urls


def batchGetURL(keyword, region):
    """
    批量抓取
    :param keyword:
    :param region:
    :return:
    """
    urls = get_joblist_urls(keyword, region)
    page = 1
    total = len(urls)
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 获取列表并保存
    rows = []
    for url in urls:
        temp = dict()
        temp['keyword'] = keyword
        temp['region'] = region
        temp['url'] = url
        temp['create_time'] = create_time
        temp['update_time'] = 0
        temp['crawled'] = 0
        rows.append(temp)

    insertAllAndShowInfo("URLS", rows)
    # 获取列表并保存


if __name__ == '__main__':
    datas = []
    keywords = [
        '产品经理',
        '运营经理',
        '数据分析师',
        '算法工程师'
    ]
    regions = [
        '北京',
        '上海',
        '广州',
        '深圳',
        '杭州',
        '成都',
        '西安',
        '武汉'
    ]
    # keyword = input("关键词:")
    # region = input("地区:")

    for keyword in keywords:
        for region in regions:
            batchGetURL(keyword, region)


