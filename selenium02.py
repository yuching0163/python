from selenium import webdriver
import re
import json

url = "https://www.ifreesite.com/population/"
xpath = '//tr[@bgcolor="#FFFFFF"]//td[@width="50%"]'

chromeDriver = r'/Users/user/AppData/Roaming/Microsoft/Windows//Start Menu/Programs/Python 3.7/chromedriver'
driver = webdriver.Chrome(chromeDriver) 
driver.maximize_window()

driver.get(url)
statedict = {}
r1 = '[a-zA-Z ]'

for element in driver.find_elements_by_xpath(xpath):
    try:
        content = element.text
        chinese_name = content.split('\n')[-1]
        english_name = content.split('|')[0]
        number = ''.join(list(filter(str.isdigit, content)))

        if number:
            country = chinese_name + " " + english_name
            if state in statedict:
                statedict[state].append({"洲名" : state, "國家" : country, "人口數": number})
            else:
                statedict[state] = [{"洲名" : state, "國家" : country, "人口數": number}]
                
        elif chinese_name:
            verify = re.sub(r1, '', chinese_name)
            if verify:
                state = verify + " "
            else:
                state+=english_name

    except OSError:
        print('發生OSError!')
        break;

txt = open("country.txt",'w+',encoding="utf-8")

for state in statedict:
    statedict[state].sort(key=lambda k:-int(k["人口數"].replace(",","")))
    for country in statedict[state]:
        txt.write(json.dumps(country, ensure_ascii=False)+'\n')

txt.close()
driver.close()