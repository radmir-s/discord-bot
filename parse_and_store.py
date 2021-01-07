from bs4 import Tag, NavigableString, BeautifulSoup
import requests
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from os import remove

tail = 12


def save_image_file(image_url):
    req = requests.get(image_url)
    with open(image_url[-tail:], 'wb') as f:
        f.write(req.content)


def insert_image(image_url):
    return "\\begin{figure}[h]\\centering\\includegraphics[height=3cm]{" + image_url[-tail:] + "}\\end{figure}\n\n"


def get_text(tag):
    tag.get_text(strip=True).split()


def get_problem(amc="AMC_8", year=2014, problem_num=15):
    link = f"https://artofproblemsolving.com/wiki/index.php/{year}_{amc}_Problems/Problem_{problem_num}"
    with requests.get(link) as req:
        soup = BeautifulSoup(req.content, features="html.parser")
    problem = []
    images_links = []
    start = soup.find("p")
    while True:
        if isinstance(start, NavigableString) and start != "\n":
            problem.append(start)
        elif isinstance(start, Tag) and start.name == 'img' and start.has_attr("alt"):
            if start['alt'].startswith("[asy]") or start['alt'].endswith(".png"):
                problem.append(insert_image(start['src']))
                if start['src'].startswith("http"):
                    images_links.append(start['src'])
                else:
                    images_links.append("http:" + start['src'])
            else:
                problem.append(start['alt'])
        start = start.next_element
        if isinstance(start, Tag):
            if start.has_attr("id"):
                if "Solution" in start["id"] or "toc" in start["id"]:
                    break
    amc = amc.replace("_", " ")
    problem.insert(-1, "\\newline \\indent")
    return f"{year} {amc} Problem {problem_num} \\newline \\indent " + "".join(
        problem) + "\\vspace{3mm}\n\n", images_links


def get_problem_set(amc="AMC_8", y1=2018, y2=2020, p1=3, p2=5):
    problem_set = []
    images_links = []
    for y in range(y1, y2 + 1):
        print(y)
        for p in range(p1, p2 + 1):
            print(p)
            problem, links = get_problem(amc, y, p)
            problem_set.append(problem)
            images_links.extend(links)
    return problem_set, images_links


def store_problem_set(amc="AMC_8", y1=2018, y2=2020, p1=3, p2=5):
    problem_set, images_links = get_problem_set(amc, y1, y2, p1, p2)
    time_now = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
    file_name = "problem set " + time_now + ".txt"
    with open(file_name, "w") as file:
        file.write("Problem Set " + time_now + "\\vspace{3mm}\n\n")
        file.writelines(problem_set)
    for url in images_links:
        save_image_file(url)
    file_names = [file_name]
    file_names.extend([url[-tail:] for url in images_links])
    return file_names


def prepare_zip(amc="AMC_8", y1=2018, y2=2020, p1=3, p2=5):
    file_names = store_problem_set(amc, y1, y2, p1, p2)
    zip_file_name = file_names[0][:-4] + ".zip"
    zip_file = ZipFile(zip_file_name, "w")
    for file_name in file_names:
        zip_file.write(file_name, compress_type=ZIP_DEFLATED)
        remove(file_name)
    return zip_file_name


if __name__ == "__main__":
    prepare_zip(amc="AMC_8", y1=2017, y2=2020, p1=1, p2=25)
