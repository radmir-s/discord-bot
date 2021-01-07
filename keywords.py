from bs4 import BeautifulSoup
import requests

def is_keyword_in(amc="AMC_8", year=2014, problem_num=15, all_true = True, keys = []):
    link = f"https://artofproblemsolving.com/wiki/index.php/{year}_{amc}_Problems/Problem_{problem_num}"
    with requests.get(link) as req:
        soup = BeautifulSoup(req.content, features="html.parser")
    if all_true:
        for key in keys:
            all_true = key in soup.find("p").text and all_true
    else:
        for key in keys:
            all_true = key in soup.find("p").text or all_true

    return all_true

def probs_with_keywords(amc="AMC_8", y1=2005,y2=2007,p1=1,p2=3, all_true = True, keys = []):
    probs_with_keys = []
    for y in range(y1,y2+1):
        for p in range(p1,p2+1):
            if is_keyword_in(amc, y, p, all_true, keys):
                probs_with_keys.append((amc,y,p))
    return probs_with_keys

if __name__ == "__main__":
    print(probs_with_keywords(amc="AMC_8", y1=2005,y2=2015,p1=1,p2=5, all_true = True, keys = ["point"]))




