import requests
import selenium
from fyers_api import fyersModel
from fyers_api import accessToken
from fyers_api.Websocket import ws
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time
from creds import *


def get_access_token(auth_code):
    appSession = accessToken.SessionModel(client_id=app_id, secret_key=secret_key, grant_type="authorization_code")
    appSession.set_token(auth_code)
    response = appSession.generate_token()["access_token"]
    return response

def gen_auth_token():
    url= f"https://api.fyers.in/api/v2/generate-authcode?client_id={app_id}&redirect_uri={redirect_uri}&response_type=code&state=husainiscool"
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    time.sleep(5)
    driver.execute_script(f"document.querySelector('[id=fy_client_id]').value = '{client_id}'")
    driver.execute_script("document.querySelector('[id=clientIdSubmit]').click()")
    time.sleep(3)
    otp = input("enter otp recieved : ")
    otp_pin = [*otp]
    driver.execute_script(f"document.querySelector('[id=confirmOtpForm]').querySelector('[id=otp-container]').querySelector('[id=first]').value = '{otp_pin[0]}'")
    driver.execute_script(f"document.querySelector('[id=confirmOtpForm]').querySelector('[id=otp-container]').querySelector('[id=second]').value = '{otp_pin[1]}'")
    driver.execute_script(f"document.querySelector('[id=confirmOtpForm]').querySelector('[id=otp-container]').querySelector('[id=third]').value = '{otp_pin[2]}'")
    driver.execute_script(f"document.querySelector('[id=confirmOtpForm]').querySelector('[id=otp-container]').querySelector('[id=fourth]').value = '{otp_pin[3]}'")
    driver.execute_script(f"document.querySelector('[id=confirmOtpForm]').querySelector('[id=otp-container]').querySelector('[id=fifth]').value = '{otp_pin[4]}'")
    driver.execute_script(f"document.querySelector('[id=confirmOtpForm]').querySelector('[id=otp-container]').querySelector('[id=sixth]').value = '{otp_pin[5]}'")
    driver.execute_script("document.querySelector('[id=confirmOtpSubmit]').click()")
    print(otp_pin)
    time.sleep(5)
    driver.execute_script(f"document.querySelector('[id=verify-pin-page]').querySelector('[id=first]').value = '{pin[0]}'")
    driver.execute_script(f"document.querySelector('[id=verify-pin-page]').querySelector('[id=second]').value = '{pin[1]}'")
    driver.execute_script(f"document.querySelector('[id=verify-pin-page]').querySelector('[id=third]').value = '{pin[2]}'")
    driver.execute_script(f"document.querySelector('[id=verify-pin-page]').querySelector('[id=fourth]').value = '{pin[3]}'")
    driver.execute_script("document.querySelector('[id=verifyPinSubmit]').click()")
    time.sleep(3)
    newurl = driver.current_url
    auth_code = newurl[newurl.index('auth_code')+10:newurl.index('&state')]
    # print(auth_code)
    driver.quit()
    return auth_code

def main():
    global fyers

    auth_code=gen_auth_token()
    print(f"auth token == {auth_code}")
    access_token = get_access_token(auth_code)
    print(f"access token == {access_token}")
    fyers= fyersModel.FyersModel(token=access_token, client_id=client_id)
    symbol = "NSE:SBIN-EQ"
    quotes = fyers.quotes(symbols = symbol)
    lts = quotes['ip']
    print(lts)
    # lol account got blocked

if __name__ == "__main__":
    main()