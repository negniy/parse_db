import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "http://185.244.219.162/phpmyadmin" ## объединить
LOGIN_URL = f"{BASE_URL}/index.php"
SQL_URL = f"{BASE_URL}/index.php"

USERNAME = "test"
PASSWORD = "JHFBdsyf2eg8*"
TOKEN = None
SESSION = None

def login_to_phpmyadmin(session):
    payload = {
        "set_session": SESSION,
        "pma_username": USERNAME,
        "pma_password": PASSWORD,
        "server": 1,
        "route": "/",
        "token": TOKEN
    }

    response = session.post(LOGIN_URL, data=payload)

    if not response.history and response.history[0].status_code != 302:
        raise Exception("Авторизация не удалась")
    
    print("Успешный вход в phpMyAdmin")
    
    return session

def get_token(r):
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find(attrs={"name": "token"})["value"]
    if not token:
        raise Exception("Не удалось найти токен")
    return token

def get_table(session):
    params = {
        "route": "/sql",
        "server": "1",
        "db": "testDB",
        "table": "users",
        "pos": "0"
    }

    response = session.get(SQL_URL, params=params)


    if response.status_code != 200:
        raise Exception("Не удалось получить данные таблицы")
    
    soup = BeautifulSoup(response.text, "html.parser")
    tbody = soup.find("tbody")
    if not tbody:
        print("Данные не найдены")
    else:
        rows = tbody.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            values = [col.get_text(strip=True) for col in columns if col.get("class") is None or "data" in col.get("class")]
            print(values)
        
    return

def main():
    global SESSION
    global TOKEN
    
    session = requests.Session()
    r = session.get(BASE_URL)

    SESSION = r.cookies.get("phpMyAdmin")
    TOKEN = get_token(r)
    session = login_to_phpmyadmin(session=session)
    get_table(session=session)
    

if __name__ == "__main__":
    main()
