from bs4 import Tag, NavigableString, BeautifulSoup
import requests
from datetime import datetime


def stop_tag(tag):
    if tag.has_attr("id"):
        return tag["id"] == "Solution_1" or tag["id"] == "Solution"
    return False


def get_text(tag):
    tag.get_text(strip=True).split()


time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")


def write_txt_file(problem_set):
    time_now = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
    with open("problem set " + time_now + ".txt", "w") as file:
        file.write("Problem Set " + time_now + "\\vspace{3mm}\n\n")
        file.writelines(problem_set)


def get_problem(amc="8", year=14, problem_num=15):
    year_str = str(year) if year>9 else "0"+str(year)
    link = "https://artofproblemsolving.com/wiki/index.php/20" + year_str + "_AMC_" + amc + "_Problems/Problem_" + str(
        problem_num)
    with requests.get(link) as req:
        soup = BeautifulSoup(req.content, features="html.parser")
    problem = []
    start, stop = soup.find("p"), soup.find(stop_tag)
    while start != stop:
        if isinstance(start, NavigableString):
            problem.append(start)
        elif isinstance(start, Tag) and start.name == 'img' and start.has_attr("alt"):
            if start['alt'][:5] == "[asy]":
                problem.append('\n\\href{' + start['src'] + '}{Picture}\n')
            else:
                problem.append(start['alt'])
        start = start.next_element
    return "20" + year_str + " AMC " + amc + " Problem " + str(problem_num) + " \\newline \\indent " + "".join(
        problem) + "\\vspace{3mm}"


def get_problem_set(amc, y1, y2, p1=1, p2=25):
    problem_set = []
    for y in range(y1, y2 + 1):
        for p in range(p1, p2 + 1):
            problem_set.append(get_problem(amc, y, p))
    return problem_set


if __name__ == "__main__":
#    write_txt_file(get_problem_set("8", 10, 15,2, 4))
    print(get_problem(amc="8", year=19, problem_num=1))