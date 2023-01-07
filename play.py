import asyncio, re, os, csv, time
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright,email,direk,nmFile)-> None:
  browser = playwright.firefox.launch(headless=True, slow_mo=500)
  context = browser.new_context()
  context.grant_permissions(['geolocation', 'notifications'])
  page = context.new_page()
  page.goto("https://grivy.app/login")
  try:page.wait_for_selector('.cdk-overlay-container',timeout=10000)
  except:page.reload(); page.wait_for_selector('.cdk-overlay-container',timeout=10000)
  if page.query_selector('//*[@class="confirm-item"]'): page.locator('//*[@class="confirm-item"]').click()
  try:page.wait_for_selector('.login-container',timeout=3000)
  except:page.reload(); page.wait_for_selector('.login-container',timeout=3000)
  with page.expect_popup() as popup_info: page.locator('//*[text()="Google"]').click()
  newPage = popup_info.value
  try:
    newPage.wait_for_selector('input[id="identifierId"]',timeout=2000)
    newPage.locator('input[id="identifierId"]').fill(email)
  except:
    newPage.reload()
    newPage.wait_for_selector('input[type="email"]',timeout=3000)
    newPage.locator('input[type="email"]').fill(email)
  newPage.wait_for_timeout(500)
  newPage.keyboard.press('Enter')
  newPage.wait_for_timeout(1000)
  if newPage.query_selector('span.jibhHc') != None:
    newPage.close()
    browser.close()
    return 'No'
  newPage.wait_for_selector('input[type="password"]',timeout=3000)
  newPage.locator('input[type="password"]').fill("t3rs3r4h")
  newPage.wait_for_timeout(500)
  newPage.keyboard.press('Enter')
  for x in range(100):
    newPage.wait_for_timeout(100)
    result = 'No'
    try:
      if newPage.url.find('challenge/iap') != -1:
        mmm = open("kenaveriv.txt", "a", newline="")
        mmm.write(f"{email.strip()}\n")
        mmm.close()
        context.close()
        browser.close()
        return result
    except:pass
    try :
      if newPage.query_selector("#accept"):
        newPage.locator("#accept").click()
    except:pass
    try:
      if newPage.query_selector("#confirm"):
        newPage.locator("#confirm").click()
    except:pass
    try:
      result = re.findall("ya29.*?quot",newPage.content())[0].replace("\&quot",'')
      break
    except:pass
  newPage.wait_for_timeout(3000)
  if result != 'No': context.storage_state(path=f"MyCookies/{direk}/{nmFile}.json")
  context.close()
  browser.close()
  return result


def saved(numb,email,token):
  filer = open("grivy.csv", "a",newline="")
  filer.write(f"{numb+1},{email.strip()},{token.strip()}\n")
  filer.close()
  print(numb+1,email)

if __name__ == '__main__':
  fox = open("user.txt","r").readlines()
  for numb in range(len(fox)):
    if numb%50 == 0:
      os.system('clear')
    email = fox[numb].strip()
    direk = email.split('@')[1]
    nmFile = email.split('@')[0]
    if os.path.isdir("MyCookies") == False:
      os.mkdir("MyCookies")
    if os.path.isdir(f"MyCookies/{direk}") == False:
      os.mkdir(f"MyCookies/{direk}")
    with sync_playwright() as playwright:
      token = run(playwright,email,direk,nmFile)
    if token != 'No':
      saved(numb, email, token)

