import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
browser.get(url)
# title,ratings,year,url,rank,inside_desc


def getTitles():

    xp = "//td[@class='titleColumn']//a"
    titles_list = browser.find_elements(By.XPATH, xp)
    titles = []
    for x in titles_list:
        if x.text == "Winnie-The-Pooh: Blood and Honey":
            continue

        titles.append(x.text)

    return titles


def getUrls():
    xp = "//td[@class='titleColumn']//a"
    urls_list = browser.find_elements(By.XPATH, xp)
    urls = []
    i = 1
    for x in urls_list:
        if x.text == "Winnie-The-Pooh: Blood and Honey":
            continue

        urls.append(x.get_attribute('href'))
        i += 1
        
    return urls


def getRatings():
    path = 'td.ratingColumn.imdbRating'
    ratings_list = browser.find_elements(By.CSS_SELECTOR, path)
    ratings = []
    for x in ratings_list:
        ratings.append(x.text.replace('\n', ''))
    return ratings


def getYears():
    path = 'td.titleColumn>span'
    years_list = browser.find_elements(By.CSS_SELECTOR, path)
    years = []
    for x in years_list:
        years.append(x.text)
    return years


def getDescriptions(urls):

    descriptions = []

    for x in urls:
        browser.get(x)
        xp = "//span[@data-testid='plot-l']"
        description_list = browser.find_element(By.XPATH, xp)
        descriptions.append(description_list.text)

    return descriptions


def getCsv(titles, urls, ratings, years, descriptions):
    with open('imdb.csv', 'w', newline='') as file:
        fieldnames = ["rank", "titles", "urls",
                      "ratings", "years", "descriptions"]
        i = 0
        j = 1
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for x in descriptions:
            writer.writerow(
                {'rank': j, 'titles': titles[i], 'urls': urls[i], 'ratings': ratings[i], 'years': years[i], 'descriptions': x})
            j += 1
            i += 1


def main():
    titles = urls = ratings = years = descriptions = []
    titles = getTitles()
    urls = getUrls()
    ratings = getRatings()
    years = getYears()
    descriptions = getDescriptions(urls)
    getCsv(titles, urls, ratings, years, descriptions)
    browser.close()


main()
