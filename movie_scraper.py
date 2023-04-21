import requests
import csv
from bs4 import BeautifulSoup


def getData():
    url = 'https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=470df400-70d9-4f35-bb05-8646a1195842&pf_rd_r=KK7BN9R3FJ0KSWTQG188&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_2'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    with open('popular_movies.html', 'w') as f:
        f.write(soup.prettify())


record = []


def fetch():
    with open('popular_movies.html') as f:
        content = f.read()
        try:
            soup = BeautifulSoup(content, 'html.parser')
            movies = soup.find('tbody', class_='lister-list').find_all('tr')

            for index, movie in enumerate(movies):
                name = movie.find('td', class_='titleColumn').a.text.strip()
                year = movie.find(
                    'td', class_='titleColumn').span.text.strip().strip('()')
                rank = movie.find(
                    f'td', class_='ratingColumn imdbRating').strong
                if rank is not None:
                    rank = rank.text.strip()
                poster = movie.find('td', class_='posterColumn').a.img['src']
                record.append([index+1, name, year, rank, poster])

        except Exception as e:
            print(e)


def csv_file():
    with open('popular_movies.csv', 'w') as obj:
        f = csv.writer(obj)
        f.writerow(['SN', 'rank', 'name', 'year', 'rating', 'poster'])
        for item in record:
            sn = item[0]
            name = item[1]
            year = item[2]
            rank = item[3]
            poster = item[4]
            data = [sn, name, year, rank, poster]
            f.writerow(data)


if __name__ == '__main__':
    getData()
    fetch()
    csv_file()
