from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("./chromedriver")

url = "https://movie.naver.com/"
driver.get(url)
time.sleep(3)

##영화 랭킹
driver.find_element(By.CSS_SELECTOR, "a.menu03").click()
time.sleep(2)


wantdict = {}
title = []
n = 1
order = input("영화 랭킹 순서를 선택하세요 (조회순/ 평점순) : ")
if order == "조회순":
    print("<<TOP10-조회순>>")
    for element in driver.find_elements(By.CSS_SELECTOR, "div.tit3")[:10]:
        print(n, ".", element.text)
        title.append(element.text)
        n +=1
    
elif order == "평점순":
    print("<<TOP10-평점순>>")
    driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div/div/div/div[1]/div[1]/ul/li[2]/a/img").click()
    time.sleep(1)
    for element in driver.find_elements(By.CSS_SELECTOR, "div.tit5")[:10]:
        print(n, ".", element.text)
        title.append(element.text)
        n +=1
        
else:
    print("잘못된 입력")


driver.find_element(By.CSS_SELECTOR, "a.menu01").click()    #다시 홈으로
time.sleep(3)


for i in range(10):
    wantdict[i+1] = title[i]
#print(wantdict[5])


##원하는 영화 입력
want = input("원하는 영화 제목의 번호(1~10)를 선택하세요. : ")
keyword = wantdict[int(want)]
search = driver.find_element(By.CSS_SELECTOR, "input#ipt_tx_srch")
search.send_keys(keyword)
driver.find_element(By.CSS_SELECTOR, "button.btn_srch").click()
time.sleep(3)


driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div/div/div/div[1]/ul[2]/li/dl/dt/a").click()
time.sleep(2)


#원하는 영화 정보
driver.find_element(By.XPATH, "/html/body/div/div[4]/div[3]/div[1]/div[3]/ul/li[5]/a").click()  #평점 클
time.sleep(2)


netizen = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[1]/div[3]/div[2]/a").text
audience = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/a/div/span/span").text
#reporter = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/span").text
print("<<'",keyword,"'의 평점>>", "\n")
print("네티즌 평점: ", netizen,'점','\n',audience)#, '기자&평론가 평점: ',reporter)




#리뷰
print('\n\n',"<<'",keyword,"'의 리뷰>>", '\n')
time.sleep(2)


print("스포 없음!")
for i in range(10):
    path = "/html/body/div/div/div[5]/ul/li["+str(i+1)+"]/div[2]/p/span[2]"
    driver.switch_to.frame("pointAfterListIframe")
    review = driver.find_element(By.XPATH, path)
    print(i+1, '.' , review.text)
    driver.back()
    driver.find_element(By.XPATH, "/html/body/div/div[4]/div[3]/div[1]/div[3]/ul/li[5]/a").click()


driver.close()