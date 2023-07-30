from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        link = request.form['search-bar']
        data = scrape(link)
        return render_template('index.html', text=data[0], stat=data[1], title=data[2])

def scrape(link):
    full = []

    link = 'https://quizizz.com/print/quiz/' + sorted(link.split('/'), key=len)[-1]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-3d-apis")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'")

    service = Service("/opt/render/project/.render/chrome/opt/google/chrome/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(link)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    status = 'success'
    title = 'None'
    final = []

    try:
        others_btn = list(WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-1.flex.h-13 button'))))
        others_btn[len(others_btn)-1].click()
        title = driver.find_element(By.CSS_SELECTOR, '.font-normal.leading-6.text-4').text
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'switch__label'))).click()
        data = driver.find_elements(By.CSS_SELECTOR, ".p-b-a-always > .flex")
        correct = driver.find_elements(By.CSS_SELECTOR, ".grid.gap-4.m-4.grid-cols-4 .flex")

        for i in range(len(data)):
            ques = data[i].find_element(By.CSS_SELECTOR, ".flex.flex-col.w-full").text
            ans = [j.text for j in data[i].find_elements(By.CSS_SELECTOR, '.flex.flex-wrap.w-full .w-option-text')]
            if ans == []:
                ans = [f"""<img src="{j.get_attribute('src')}"></img>""" for j in data[i].find_elements(By.CSS_SELECTOR, '.flex.flex-wrap.w-full .flex img')]
            for j in range(len(ans)):
                ans[j] = alphabet[j] + '. ' + ans[j]
            cor = (correct[i].text.replace('\n', '').replace(' ', '')[(correct[i].text).find('.')+1:].strip()).split(',')
            lst = [str(i+1), ques, ans, []]

            for j in cor:
                if j == 'a':
                    lst[3].append(ans[0])
                elif j == 'b':
                    lst[3].append(ans[1])
                elif j == 'c':
                    lst[3].append(ans[2])
                elif j == 'd':
                    lst[3].append(ans[3])
                elif j == 'e':
                    lst[3].append(ans[4])
                else:
                    lst[3].append(cor)
            
            final.append(lst)

        if full != None:
            for i in final:
                print(i[0] + '. ' + i[1] + '\n' + '\n'.join(i[2]) + '\n\n')
        else:
            for i in final:
                print(i[0] + '. ' + i[1] + '\n' + ','.join(i[3]) + '\n\n')
    
    except Exception:
        status = 'failed'
    
    finally:
        driver.close()
        return [final, status, title]

if __name__ == '__main__':
    app.run()