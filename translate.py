import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

chromeDiverPath = "./lib/chromedriver"
xPath = "/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/p[2]"
translateApi = "https://fanyi.baidu.com/#en/zh/"
filePath = input("请输入cmdline文件的绝对路径: ")
driver = webdriver.Chrome(service=Service(chromeDiverPath))
res = list()

with open(file=filePath, mode='r', encoding="utf-8") as fileObject:
    text = fileObject.read()
    dataList = re.findall(r'help="(.*)"', text)

for data in dataList:
    driver.get(translateApi + data)
    driver.implicitly_wait(10)
    time.sleep(1) # 最低延时 0.5，否则容易崩溃
    cn = driver.find_element(By.XPATH, xPath).text
    print(cn)
    res.append(cn)

for index in range(len(dataList)):
    text = text.replace(dataList[index], res[index])

# 删除空格(%20 --Url dencoding--> 空格)
text = text.replace("%20", "")
# 替换引号(%22 --Url dencoding--> ")
text = text.replace("%22", '"')

with open("cmdline_cn.py","wb",encoding="utf-8") as fileObject:
    fileObject.write(text)