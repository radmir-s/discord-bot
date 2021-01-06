from bs4 import Tag, NavigableString, BeautifulSoup
import requests
from datetime import datetime


def save_image_file(image_url):
    req = requests.get(image_url)
    with open(image_url[-35:], 'wb') as f:
        f.write(req.content)


def insert_image(image_url):
    return "\\begin{figure}[h]\\centering\\includegraphics[height=4cm]{" + image_url[-35:] + "}\\end{figure}\n\n"


def stop_tag(tag):
    if tag.has_attr("id"):
        return tag["id"] == "Solution_1" or tag["id"] == "Solution"
    return False


def get_text(tag):
    tag.get_text(strip=True).split()


def store_problems(problem_set):
    time_now = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
    with open("problem set " + time_now + ".txt", "w") as file:
        file.write("Problem Set " + time_now + "\\vspace{3mm}\n\n")
        file.writelines(problem_set)


def get_problem(amc="8", year=14, problem_num=15):
    link = f"https://artofproblemsolving.com/wiki/index.php/20{year:02}_AMC_{amc}_Problems/Problem_{problem_num}"
    with requests.get(link) as req:
        soup = BeautifulSoup(req.content, features="html.parser")
    problem = []
    images_links = []
    start, stop = soup.find("p"), soup.find(stop_tag)
    while start != stop:
        if isinstance(start, NavigableString):
            problem.append(start)
        elif isinstance(start, Tag) and start.name == 'img' and start.has_attr("alt"):
            if start['alt'][:5] == "[asy]":
                problem.append(insert_image(start['src']))
                print(start['src'])
                images_links.append("http:" + start['src'])
            else:
                problem.append(start['alt'])
        start = start.next_element
    return f"20{year:02} AMC {amc} Problem {problem_num} \\newline \\indent " + "".join(
        problem) + "\\vspace{3mm}", images_links


def get_problem_set(amc, y1, y2, p1=1, p2=25):
    problem_set = []
    for y in range(y1, y2 + 1):
        for p in range(p1, p2 + 1):
            problem_set.append(get_problem(amc, y, p))
    return problem_set


def store_a_problem(amc="8", year=12, problem_num=1):
    problem, image_links = get_problem(amc="8", year=14, problem_num=15)
    for image_url in image_links:
        save_image_file(image_url)
    with open(f"20{year:02} AMC {amc} Problem {problem_num}.txt", "w") as file:
        file.write(f"20{year:02} AMC {amc} Problem {problem_num}" + "\\vspace{3mm}\n\n")
        file.writelines(problem)


if __name__ == "__main__":
    store_a_problem()
