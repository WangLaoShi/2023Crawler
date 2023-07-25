# //span[@class="position-head-wrap-name"]/span[1] 标题
# //dd[@class="job-advantage"]/span 职位诱惑四字
# //dd[@class="job_bt"]/h3 职位描述
# //span[@class="position-head-wrap-name"]/span[2] 薪资
# //dd[@class="label-wrapper"]/h3 附加信息
# //dd[@class="job-address clearfix"]/h3 工作地址
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions, DesiredCapabilities
from selenium.webdriver.common.by import By
from urllib import parse

# import datetime
# import requests
# import sys
# def compare_dates(date_str):
#     net_data = datetime.datetime.strptime(requests.get('http://www.ntp.org').headers['Date'], '%a, %d %b %Y %H:%M:%S %Z').date()
#     print(net_data)
#     if net_data > datetime.datetime.strptime(date_str, '%Y-%m-%d').date():
#         # 如果当前日期大于目标日期，则退出程序
#         sys.exit(0)
# compare_dates('2023-5-6')


options = ChromeOptions()

# prefs = {
#     'profile.default_content_setting_values': {
#         'images': 2,
#     }
# }
# options.add_experimental_option('prefs', prefs)
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# ca = DesiredCapabilities().CHROME
# ca['pageLoadStrategy'] = 'none'
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
driver = Chrome(executable_path='chromedriver', options=options)

def get_data():
    data = {}
    while True:  # 等待标题出现
        try:
            bts = driver.find_elements(By.XPATH, '//span[contains(@class, "position-head-wrap-name")]/span[1]')
            bt = "".join([item.text for item in bts])
            if bt != "":
                break
        except:
            time.sleep(0.05)
    time.sleep(0.2)
    try:
        zwyhs = driver.find_elements(By.XPATH, '//dd[@class="job-advantage"]/p')
        zwyh = "".join([item.text for item in zwyhs])
    except:
        zwyh = "无"
    try:
        xzs = driver.find_elements(By.XPATH, '//span[@class="position-head-wrap-name"]/span[2]')
        xz = "".join([item.text for item in xzs])
    except:
        xz = "无"

    try:
        job_description_elements = driver.find_elements(By.XPATH, '//dd[@class="job_bt"]/div')
        job_description = "".join([item.text for item in job_description_elements])
    except:
        job_description = "无"

    try:
        additional_info_elements = driver.find_elements(By.XPATH, '//dd[@class="label-wrapper"]/ul')
        additional_info = "".join([item.text for item in additional_info_elements])
    except:
        additional_info = "无"

    try:
        job_address_elements = driver.find_elements(By.XPATH, '//dd[@class="job-address clearfix"]/div')
        job_address = "".join([item.text for item in job_address_elements])
    except:
        job_address = "无"

    try:
        group_elements = driver.find_elements(By.XPATH, '//dl[@class="job_company"]//em')
        group = "".join([item.text for item in group_elements])
    except:
        group = "无"

    try:
        group_info_elements = driver.find_elements(By.XPATH, '//ul[@class="c_feature"]/li')
        group_info = "".join([item.text for item in group_info_elements])
    except:
        group_info = "无"

    data["zwyh"] = zwyh
    data["job_description"] = job_description
    data["additional_info"] = additional_info
    data["job_address"] = job_address
    data["group"] = group
    data["xz"] = xz
    data["bt"] = bt
    data["group_info"] = group_info

    return data

def get_urls(key, dq):
    driver.get("https://www.lagou.com/jobs/list_"+parse.quote(key)+"?city="+parse.quote(dq))
    urls = []
    o = ''
    while True:
        try:
            u = [i.get_attribute('href') for i in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="s_position_list "]/ul[@class="item_con_list"]//a[@class="position_link"]')))]
        except:
            time.sleep(0.02)
            continue
        if u[0] != o:
            # print(u)
            urls.extend(u)
            o = u[0]
            ti = time.time()
            while time.time()-ti < 5:
                try:
                    driver.find_element(By.XPATH, '//span[@class="pager_next "]').click()
                    time.sleep(1)
                    break
                except:
                    pass
            else:
                return urls

if __name__ == '__main__':
    datas = []
    g = input("关键词:")
    d = input("地区:")
    uu = get_urls(g, d)
    for ur in uu:
        driver.get(ur)
        d = get_data()
        datas.append(d)
        time.sleep(0.5)
        print(d)














