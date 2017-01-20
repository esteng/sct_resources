import re
import mechanize






URL = "http://lcorp.ulif.org.ua/dictua/"

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(URL)



for i in range(10):
    html = response.read()
    # print("Page %d :" % i, html)

    br.select_form(nr=0)
    # print( br.form)
    br.set_all_readonly(False)

    with open("test.html",'w') as f2:
        f2.write(html)

    mnext = re.search("""<a href="javascript:__doPostBack('ctl00\$ContentPlaceHolder1\$dgv','Select\$\d+)'""", html)
    if not mnext:
        print("not found")
        break
    br["__EVENTTARGET"] = mnext.group(1)
    br["__EVENTARGUMENT"] = mnext.group(2)
    br.find_control("btnSearch").disabled = True
    response = br.submit()
    print(response)

