import requests
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import datetime
import time
import os
import pyautogui
#Code tren server
# Xóa tất cả các tệp tin trong thư mục 'photos'
folder_path = 'C:\\Users\\Administrator\\Desktop\\Bot_telegram\\Image\\'
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

# Setup Chrome driver
options = ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='C:\\Users\\Administrator\\Desktop\\Bot_telegram\\chromedriver.exe') # path to driver file
driver.set_window_size(1920, 1080)
#pyautogui.press('f11')

# Setup Telegram bots
TELEGRAM_BOT_TOKENS ='5707243837:AAGSdNhMdzr7Cqodq4AT1Y2pCp1AUIriHC8' #'6096572878:AAGZZuQwkB5ngjXr4lxZI4E5ykmu29APpGM'
TELEGRAM_CHAT_IDS =[ '-834581094', # Unigap dask board
                     '-834581094', # Unigap dask board
                     '-834581094', # Unigap dask board
                     '-834581094', # Unigap dask board
                     '-1001878000161', # UniGap_MKT Team
                     '-1001878000161' # UniGap_MKT Team
                     ] 

# URL list to capture screenshots
DRIVE_URLS = [ 
            'https://docs.google.com/spreadsheets/d/1FhzxWnDgFSJaoiRWQ96zoHVyMmJMp2050-tn1JQ-qBg/edit#gid=2135939179', # Stage 1. DA fundamental
            'https://docs.google.com/spreadsheets/d/1FhzxWnDgFSJaoiRWQ96zoHVyMmJMp2050-tn1JQ-qBg/edit#gid=567083581', # Stage 2 - Application
            'https://docs.google.com/spreadsheets/d/10lK_snr6RgQsEHvz3mu6JvyeP_3x3BqyX666fyKwcK8/edit#gid=0', # PDP Dashboard            
            'https://docs.google.com/spreadsheets/d/1pjHb2cR1EWI8cT2S8MHJ3lyy8j9fmtwH6zyrDj1k6qo/edit#gid=1774663868',#DEC Performance Dashboard'
            'https://docs.google.com/spreadsheets/d/1Fi2j7L2GNosqO8wp5HSCRYfkM4UgktvjAROYQUOPU5Y/edit#gid=1132737363',#Standup Meeting Channel
            'https://docs.google.com/spreadsheets/d/1Fi2j7L2GNosqO8wp5HSCRYfkM4UgktvjAROYQUOPU5Y/edit#gid=387523723']  #Sale Dashboard
MESSAGE =['Stage 1. DA fundamental','Stage 2 - Application','PDP Dashboard','DEC Performance Dashboard','Channel Dashboard','Sale Dashboard']
PHOTO_PATHS = [f'C:\\Users\\Administrator\\Desktop\\Bot_telegram\\Image\\{url.split("/")[-1]}_{datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.png' for url in DRIVE_URLS]


def capture_url(url, photo_path):
    # Open Google Drive URL
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)  # wait for 3 seconds
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # Take screenshot and save to local path
    driver.save_screenshot(photo_path)

def main():
    # Capture screenshots of all Google Drive URLs
    for url, photo_path in zip(DRIVE_URLS, PHOTO_PATHS):
        capture_url(url, photo_path)
        
    
    # Send captured screenshots to Telegram groups
    for chat_id, message, photo_path in zip( TELEGRAM_CHAT_IDS, MESSAGE, PHOTO_PATHS):
        with open(photo_path, 'rb') as f:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKENS)
            bot.send_photo(chat_id=chat_id, photo=f, caption=message)
            send = requests.post('https://api.telegram.org/bot'+ TELEGRAM_BOT_TOKENS + '/sendPhoto?chat_id=' + chat_id + '&caption=' + message, files={'photo': f})
#    pyautogui.press('f11')
    driver.quit()


if __name__ == '__main__':
    main()
