import re
from playwright.sync_api import Playwright

#* MAIN CONTROLLER
def start_bot(playwright: Playwright, arr_keywords) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="state.json")
    
    page = context.new_page()
    page.goto("https://bumble.com/app")

    date_page(page)
    page.wait_for_timeout(3000)
    date_swipe(page)
    bff_page(page)
    page.wait_for_timeout(3000)
    just_swipe(page, arr_keywords)
    bizz_page(page)
    page.wait_for_timeout(3000)
    just_swipe(page, arr_keywords)
    date_page(page)

    context.close()
    browser.close()
    exit()

def get_cookie(playwright, email, password, fa):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://bumble.com/get-started")
    
    with page.expect_popup() as popup_info:
        page.click("div[role=\"button\"]:has-text(\"Continue with Facebook\")")
    page1 = popup_info.value
    
    # Fill Email
    page1.click("input[name=\"email\"]")
    page1.fill("input[name=\"email\"]", email)
    
    # Fill Password
    page1.press("input[name=\"email\"]", "Tab")
    page1.fill("input[name=\"pass\"]", password)

    # Fill 2FA
    with page1.expect_navigation():
        page1.press("input[name=\"pass\"]", "Enter")
    
    page1.fill("[placeholder=\"Login code\"]", fa)
    
    with page1.expect_navigation():
        page1.press("[placeholder=\"Login code\"]", "Enter")

    with page1.expect_navigation():
        page1.click("text=Continue")

    page1.close()
    page.wait_for_timeout(2000)
    context.storage_state(path="state.json")
    context.close()
    browser.close()

#* CHANGE PAGE
def bff_page(page):
    # Click Profile
    page.click("div[role=\"button\"]")
    # Click Settings
    page.click("div[role=\"button\"]:has-text(\"Settings\")")
    # Click Choose Mode
    page.click("span[role=\"button\"]")

    # Click BFF
    page.click("div[role=\"button\"]:has-text(\"Make new friends at every stage of your life\")")
    # Click Confirm
    page.click("div[role=\"button\"]:has-text(\"Continue with BFF\")")
    # Back to Main
    page.click(".page__content-header-menu-item > span")
    
def bizz_page(page):
    # Click Profile
    page.click("div[role=\"button\"]")
    # Click Settings
    page.click("div[role=\"button\"]:has-text(\"Settings\")")
    # Click Choose Mode
    page.click("span[role=\"button\"]")

    # Click Bizz
    page.click("div[role=\"button\"]:has-text(\"Move your career forward the modern way\")")
    # Click Continue
    page.click("div[role=\"button\"]:has-text(\"Continue with Bizz\")")
    # Back to Main
    page.click(".page__content-header-menu-item > span")

def date_page(page):
    # Click Profile
    page.click("div[role=\"button\"]")
    # Click Settings
    page.click("div[role=\"button\"]:has-text(\"Settings\")")
    # Click Choose Mode
    page.click("span[role=\"button\"]")
    
    # Click Date
    page.click("div[role=\"button\"]:has-text(\"Find that spark in an empowered community\")")
    # Click Continue
    page.click("div[role=\"button\"]:has-text(\"Continue with Date\")")
    # Back to Main
    page.click(".page__content-header-menu-item > span")

#* DECISION
def swipe(decision, p):
    if decision:
        p.click("[aria-label=\"Like\"]")
    else:
        p.click("[aria-label=\"Pass\"]")

def looking_for(str, keyword, index):
    return bool(re.search(str, keyword[index].inner_text()))

def job_title(search_list, tag):
    for keyword in search_list:
        if bool(re.search(keyword, tag.inner_text().lower())):
            print("Job: ", tag.inner_text())
            return True
    return False

#* ACTION
def date_swipe(page, relationship=True, not_sure_yet=True, casual=True, verified=False):
    num = 0
    while True:
        # Max out matches
        end = page.query_selector(".cta-box__title > span")
        if end is not None:
            break
        if verified:
            v = page.query_selector(".encounters-story-profile__verification")
            if v is None:
                swipe(False, page)
                
        k = page.query_selector_all("div.pill__title > div")

        for i in range(len(k)):
            if relationship:
                if looking_for("relationship", k, i):
                    swipe(True, page)
                    print(k[i].inner_text())
                    continue
            if not_sure_yet:
                if looking_for("know yet", k, i):
                    swipe(True, page)
                    print(k[i].inner_text())
                    continue
            if casual:
                if looking_for("Something casual", k, i):    
                    swipe(True, page)
                    print(k[i].inner_text())
                    continue

        end = page.query_selector(".cta-box__title > span")
        if end is not None:
            break
        swipe(False, page)
        page.wait_for_timeout(1000)
        num += 1
        print(num)

def just_swipe(page, arr_keywords):
    while True:
        end = page.query_selector(".cta-box__title > span")
        if end is not None:
            break
        keyword = page.query_selector(".encounters-story-profile__occupation")
        if keyword is None:
            swipe(False, page)
        else:
            r = job_title(arr_keywords, keyword)
            swipe(r, page)
        
        match = page.query_selector(".action .text-break-words")
        if match is not None:
            page.click(".action .text-break-words")
        page.wait_for_timeout(1000)
        continue

def update_decision(v):
    if v.lower() == "true":
        return True
    else:
        return False