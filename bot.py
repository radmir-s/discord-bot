from bs4 import Tag, NavigableString, BeautifulSoup
import requests
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
import discord
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


client = discord.Client()
with open('token.txt', 'r') as reader:
    token = reader.read()

amc = y1 = y2 = p1 = p2 = None


@client.event
async def on_ready():
    print(f'{client.user} is ready!')


@client.event
async def on_message(message):
    global amc, y1, y2, p1, p2
    if message.author == client.user:
        return

    if message.content.lower().startswith('hey'):
        await message.channel.send(
            "Hey! Type an AMC you are interested in. \nExample: amc 8 (or amc 10a, ..., amc 12b)")

    if message.content.upper() in ("AMC 8", "AMC 10A", "AMC 10B", "AMC 12A", "AMC 12B"):
        amc = message.content.upper().replace(" ", "_")
        await message.channel.send(
            'Type a period of the years. (min: 1999, max:2020)\nExample: year 2007 2013')

    if message.content.lower().startswith('year') and message.content.count(' ') == 2:
        y1, y2 = message.content.split()[1:3]
        if y1.isnumeric() and y2.isnumeric():
            y1 = max(1999, int(y1))
            y2 = min(2020, int(y2))
            await message.channel.send('Type a problems range. (min: 1, max: 25)\nExample: range 3 21')

    if message.content.lower().startswith('range') and message.content.count(' ') == 2:
        p1, p2 = message.content.split()[1:3]
        if p1.isnumeric() and p2.isnumeric():
            p1 = max(1, int(p1))
            p2 = min(25, int(p2))
            await message.channel.send("Type 'gen' to generate the problem set")

    if p1 and amc:
        if p1 < 2003 and amc != "AMC_8":
            p1 = max(2000, p1)
            p2 = max(2000, p2)
            amc = "AMC_10" if amc[5] == "0" else "AMC_12"

    if message.content.lower() == "gen":
        print(amc, y1, y2, p1, p2, message.author)
        zip_file_name = prepare_zip(amc, y1, y2, p1, p2)
        await message.channel.send(file=discord.File(zip_file_name))
        remove(zip_file_name)
        amc = y1 = y2 = p1 = p2 = None


client.run(token)
