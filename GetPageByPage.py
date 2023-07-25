import datetime
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

def get_job_detail_data():
    data = {}
    while True:  # 等待标题出现
        try:
            bts = driver.find_elements(By.XPATH, '//span[contains(@class, "position-head-wrap-name")]/span[1]')
            bt = "".join([item.text for item in bts])
            if bt != "":
                break
        except:
            time.sleep(0.05 * random.randint(1, 5))
    time.sleep(0.2 * random.randint(1, 5))
    try:
        zwyhs = driver.find_elements(By.XPATH, '//dd[@class="job-advantage"]/p')
        zwyh = "$".join([item.text for item in zwyhs])
    except:
        zwyh = "无"
    try:
        xzs = driver.find_elements(By.XPATH, '//span[@class="position-head-wrap-name"]/span[2]')
        xz = "$".join([item.text for item in xzs])
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
        group_info = "$".join([item.text for item in group_info_elements])
    except:
        group_info = "无"

    data["position_advantage"] = zwyh
    data["job_description"] = job_description
    data["additional_info"] = additional_info
    data["job_address"] = job_address
    data["company"] = group
    data["salary"] = xz
    data["title"] = bt
    data["company_info"] = group_info

    return data

def append2CSV(contentDict, fileName):
    with open(fileName, 'a') as f:
        write = csv.DictWriter(f, fieldnames=contentDict.keys())
        write.writerow(contentDict)

if __name__ == '__main__':
    # 挨个爬取，并输出到 CSV 中
    page = 0
    total = 0
    tables = db_info()
    result = db.query("SELECT * FROM URLS;")
    today = datetime.date.today()
    for row in result:
        keyword = row['keyword']
        region = row['region']
        url = row['url']
        create_time = time.time()
        print("在抓取 ",keyword," 地区 ",region," 共 ",total," 页，第",page," 页")
        page +=1
        driver.get(url)
        result = get_job_detail_data()
        result['url'] = url
        result['keyword'] = keyword
        result['region'] = region
        result['create_time'] = create_time
        time.sleep(0.5*random.randint(1,5))
        print(result)
        append2CSV(result, "Lagou-"+str(today)+".csv")
    # 挨个爬取，并输出到 CSV 中