from bs4 import BeautifulSoup
import requests

def scrape_task_links(contestnumber):
    contesturl = requests.get("http://atcoder.jp/contests/abc" + f"{contestnumber:03d}" + "/tasks")
    soup = BeautifulSoup(contesturl.text, "html.parser")
    taskurls = ["https://atcoder.jp" + td.find("a").get("href") for td in soup.findAll("td", attrs={"class":"text-center no-break"}) if td.find("a")]
    # for taskurl in taskurls:
    #     print(taskurl)
    return taskurls
    