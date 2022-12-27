from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 엑셀 처리 임포트
import xlsxwriter
 
options = Options()
# headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드
# options.add_argument('headless'); 

options.add_argument('--log-level=3')

# Excel 처리 선언
savePath = "./"
workbook = xlsxwriter.Workbook(savePath + 'crawling_result.xlsx')

# 폰트 사이즈 수정
workbook.formats[0].set_font_size(10)

# 워크 시트
worksheet = workbook.add_worksheet()

# webdriver 설정
chromedriver_autoinstaller.install()

# 옵션에서 설정한 내용을 드라이버에 저장
driver = webdriver.Chrome(options=options)

#크롬 브라우저 내부 대기 (암묵적 대기)
driver.implicitly_wait(5)
# 브라우저 사이즈
driver.set_window_size(1920,1280) 

# 열고 싶은 URL
driver.get('https://www.ddm-mall.com/store/store.php?') 

# 해당 페이지 내용 출력
# print('Page Contents : {}'.format(driver.page_source)

# 검색 결과가 렌더링 될 때까지 잠시 대기
time.sleep(2)


# 현재 페이지
curPage = 1

# 크롤링할 전체 페이지수
driver.find_element_by_css_selector('#contents > div.contentArea_wide > div > div.page_num > ul > li > a.page_next2').click()
totalpage = driver.find_element_by_css_selector('#contents > div.contentArea_wide > div > div.page_num > ul > li > a.active').text
totalpage = int(totalpage) # 정수형으로 변환


# 엑셀 행 수
excel_row = 1

# 엑셀 사이즈 지정
worksheet.set_column('A:A', 35) # 열의 너비를 35으로 설정
worksheet.set_row(0,18)         # 열의 높이를 18로 설정
worksheet.set_column('B:B', 25) # 열의 너비를 25로 설정
worksheet.set_column('C:C', 30) # 열의 너비를 30으로 설정
worksheet.set_column('D:D', 20) # 열의 너비를 20으로 설정




# 엑셀 칼럼명 지정
worksheet.write(0, 0, '매장 품목(카테고리)')
worksheet.write(0, 1, '매장명')
worksheet.write(0, 2, '층수')
worksheet.write(0, 3, '연락처')


while curPage <= totalpage:
    
    #bs4 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 페이지 다시 초기화
    driver.get('https://www.ddm-mall.com/store/store.php?')

    # 상품 리스트 선택
    str_list = soup.select('#contents > div.contentArea_wide > div > div.pro_list.width1170 > dl > dt')


    # 페이지 번호 출력
    print('----- Current Page : {}'.format(curPage), '------')
    
    for v in str_list:
        
        if v.select_one('p.tel') is None:
            category = v.select_one('p.cate > span').text.strip()
            str_nm = v.select_one('h5').text.strip()
            floor = v.select_one('p.floor').text.strip()
            phone = 'n/a'
        else:
            category = v.select_one('p.cate > span').text.strip()
            str_nm = v.select_one('h5').text.strip()
            floor = v.select_one('p.floor').text.strip()
            phone = v.select_one('p.tel').text.strip()

 
        # 엑셀 저장(텍스트)
        worksheet.write(excel_row, 0, category)
        worksheet.write(excel_row, 1, str_nm)
        worksheet.write(excel_row, 2, floor)
        worksheet.write(excel_row, 3, phone)
        worksheet.write(excel_row, 4, curPage)
        
        print(category,', ', str_nm,', ', floor, ', ', phone)
        
        # 엑셀 행 증가
        excel_row += 1
        
    # 현재 페이지 정보 가져오기
    variable = driver.current_url
    pageNum = 'page={num}'.format(num=curPage)
    url = variable + pageNum
    print(url)    
    
    # 페이지 수 증가 및 페이지 이동    
    curPage += 1    
    
    driver.get(url)

    print()

    
# 브라우저 종료
driver.close()    
 
# 엑셀 파일 닫기
workbook.close() # 저장