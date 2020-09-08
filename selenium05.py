from selenium import webdriver
import re
import json
import pandas as pd

url = "https://www.ifreesite.com/population/"
xpath = '//tr[@bgcolor="#FFFFFF"]//td[@width="50%"]'

chromeDriver = r'/Users/user/AppData/Roaming/Microsoft/Windows//Start Menu/Programs/Python 3.7/chromedriver'
driver = webdriver.Chrome(chromeDriver) 
# driver.maximize_window()

driver.get(url)
state1, country1, number1 = [],[],[]
r1 = '[a-zA-Z ]'

for element in driver.find_elements_by_xpath(xpath):
    try:
        content = element.text
        chinese_name = content.split('\n')[-1]
        english_name = content.split('|')[0]
        number = ''.join(list(filter(str.isdigit, content)))

        if number:
            country = chinese_name + " " + english_name
            state1.append(state)
            country1.append(country)
            number1.append(number)
                
        elif chinese_name:
            verify = re.sub(r1, '', chinese_name)
            if verify:
                state = verify + " "
            else:
                state+=english_name

    except OSError:
        print('發生OSError!')
        break;

statedict = {"洲名": state1,  
        "國家": country1,
        "人口數": number1
        }
select_df = pd.DataFrame(statedict)
frame_class = frame.groupby('洲名')

k = select_df.sort_index(by= '人口數' )
s = k.sort_index(by= '洲名' )

s.to_csv("country.csv", index=False, encoding="utf_8_sig")

driver.close()