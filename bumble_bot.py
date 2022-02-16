from playwright.sync_api import sync_playwright
import stdiomask
import os
from helper_function import start_bot, get_cookie, update_decision


def update_prompt(k):
    x = input(f'''
====================
Updating {k}, true or false: ''')
    return x

class BumbleBot:
    def __init__(self, date=True, bff=True, bizz=True, relationship=True, not_sure=True, casual=True, verified=True, job_keywords=[], action=0) -> None:
        self.date = date
        self.bff = bff
        self.bizz = bizz
        self.relationship = relationship
        self.not_sure = not_sure
        self.casual = casual
        self.verified = verified
        self.job_keywords = job_keywords
        self.action = action
    
    def view_config(self):
        return f'''
date:        {self.date}
bff:         {self.bff}
bizz:        {self.bizz}
relationship:{self.relationship}
not_sure:    {self.not_sure}
casual:      {self.casual}
verified:    {self.verified}
job_keywords:{self.job_keywords}'''
    
    #* ENTRY POINT
    def entry_point(self):
        try:
            if isinstance(self.job_keywords, list) and all(isinstance(el, str) for el in self.job_keywords):
                with sync_playwright() as playwright:

                    if not os.path.exists("./state.json"):
                        email = input("Email: ")
                        password = stdiomask.getpass()
                        fa = input("Login 2FA (Facebook): ")
                        get_cookie(playwright, email, password, fa)

                    start_bot(playwright, self.job_keywords)
            else:
                raise Exception("job_keywords must be a list of words (string)")
        except Exception as e:
            print(e)
    
    def run(self):
        self.action = int(input(f'''
Here are the current configuration
{self.view_config()}
====================
What would you like to do?
1: Update config
2: Start bot
3. View config
Enter: '''))
        self.config()
    
    def config(self):
        if self.action == 1:
                config = input('''
====================
Provide config in the following format: key=value,key=value...
Enter 1 to update date
Enter 2 to update bff
Enter 3 to update bizz
Enter 4 to update relationship
Enter 5 to update not_sure
Enter 6 to update casual
Enter 7 to update verified
Enter 8 to update job_keywords

Enter: ''')
                if config == "1":
                    v = update_prompt("date")
                    self.date = update_decision(v)
                    self.run()
                elif config == "2":
                    v = update_prompt("bff")
                    self.bff = update_decision(v)
                elif config == "3":
                    v = update_prompt("bizz")
                    self.bizz = update_decision(v)
                elif config == "4":
                    v = update_prompt("relationship")
                    self.relationship = update_decision(v)
                elif config == "5":
                    v = update_prompt("not_sure")
                    self.not_sure = update_decision(v)
                elif config == "6":
                    v = update_prompt("casual")
                    self.casual = update_decision(v)
                elif config == "7":
                    v = update_prompt("verified")
                    self.verified = update_decision(v)
                elif config == "8":
                    self.job_keywords = []
                    while True:
                        jkw = input('''
====================
To exit, enter 0
To remove last input, enter 1
Enter a keyword: ''')
                        if jkw == "0":
                            self.run()
                        elif jkw == "1":
                            self.job_keywords.pop()
                            print(self.job_keywords)
                        else:
                            self.job_keywords.append(jkw)
                            print(self.job_keywords)
                else:
                    print("Invalid input")
                self.run()
        elif self.action == 2:
            self.entry_point()
        elif self.action == 3:
            print(self.view_config())
            self.run()
        else:
            print(f"Invalid input: {self.action}")
            self.run()

bot = BumbleBot()
bot.run()