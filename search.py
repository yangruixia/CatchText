from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pandas as pd
from tqdm import tqdm

wait_time = 2




# 启动浏览器
driver = webdriver.Chrome()  # 这里假设使用Chrome浏览器，确保已经安装了Chrome WebDriver并配置到环境变量中

# 打开页面
driver.get("http://ccl.pku.edu.cn:8080/ccl_corpus/index.jsp#")

time.sleep(wait_time)


columns = ['ID','keyword', 'tone', 'meaning', 'source', 'sentence', 'tagged', 'entity1', 'entity2', 'entity3', 'entity4', 'entity5']

# 已经爬取的数据 计算长度

catched_data = pd.read_excel('爬虫后数据.xlsx')

where_2_start = len(catched_data)
catched_data = catched_data.values.tolist()

data = pd.read_excel('tagged演示.xlsx')

for index, row in tqdm(data.iterrows(), total=len(data), ncols=100):
    if index < where_2_start:
        # 之前爬取的不再重复爬取
        continue
    
    sentence = row.sentence

    if len(sentence) >= 20:
        sentence = sentence[:20]

    content = ''

    try:

        # 输入查询语句
        # input_box = driver.find_element(by=By.ID, value='keyword')
        input_box = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.ID, 'keyword'))
                )

        input_box.send_keys(sentence)  # 在这里替换成你要查询的语句


        time.sleep(wait_time)
        input_box.send_keys(Keys.RETURN)

        time.sleep(wait_time)

        # element = driver.find_element(by=By.LINK_TEXT, value='上下文')
        element = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.LINK_TEXT, '上下文'))
                )

        element.click()

        time.sleep(wait_time)

        # info_element = driver.find_element(by=By.ID, value='info')

        info_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'info'))
        )

        # tr_element = info_element.find_elements(by=By.TAG_NAME, value='tr')[2]

        tr_elements = WebDriverWait(info_element, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
        )

        tr_element = tr_elements[2]

        # td_element = tr_element.find_elements(By.TAG_NAME, value='td')[1]

        td_elements = WebDriverWait(tr_element, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )

        td_element = td_elements[1]

        content = td_element.text

        time.sleep(wait_time)

        homepage = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.LINK_TEXT, '普通查询'))
                )
        homepage.click()

        time.sleep(wait_time)

    except:
        driver.quit()
        time.sleep(wait_time)

        # 启动浏览器
        driver = webdriver.Chrome()  # 这里假设使用Chrome浏览器，确保已经安装了Chrome WebDriver并配置到环境变量中

        # 打开页面
        driver.get("http://ccl.pku.edu.cn:8080/ccl_corpus/index.jsp#")

        time.sleep(wait_time)


        # homepage = WebDriverWait(driver, wait_time).until(
        #             EC.presence_of_element_located((By.LINK_TEXT, '普通查询'))
        #         )
        # homepage.click()

        # time.sleep(wait_time)
        

    catched_data.append([row.ID, row.keyword, row.tone, row.meaning, content, row.sentence, row.tagged, row.entity1, row.entity2, row.entity3, row.entity4, row.entity5])

    cleaned_data = pd.DataFrame(catched_data, columns=columns)
    cleaned_data.to_excel('爬虫后数据.xlsx', index=False)

# 关闭浏览器
driver.quit()




 