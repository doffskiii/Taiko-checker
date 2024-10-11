import requests
from bs4 import BeautifulSoup
import re

# Функция для получения текста с сайта
def get_value_from_site(wallet_address):
    url = f"https://trailblazer.mainnet.taiko.xyz/claim/proof?address={wallet_address}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    
    try:
        # Выполняем GET-запрос с заголовками
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлекаем весь текст со страницы
        text = soup.get_text(strip=True)
        
        # Ищем значение "value"
        match = re.search(r'"value":"([\d.]+)"', text)  # Изменяем регулярное выражение для поиска числа
        if match:
            return match.group(1)  # Возвращаем только число
        else:
            print(f"Значение 'value' не найдено для адреса {wallet_address}")
            return None

    except Exception as e:
        print(f"Ошибка при обработке адреса {wallet_address}: {e}")
        return None

# Основной блок
def main():
    results = []
    
    # Читаем адреса из файла "Wallets"
    with open('Wallets.txt', 'r') as file:
        wallets = file.readlines()

    # Обрабатываем каждый адрес
    for wallet in wallets:
        wallet = wallet.strip()  # Убираем пробелы и символы новой строки
        if wallet:  # Проверяем, что адрес не пустой
            value = get_value_from_site(wallet)
            if value is not None:
                results.append(f"{wallet}: {value}")

    # Записываем результаты в файл "Results.txt"
    with open('Results.txt', 'w') as file:
        for result in results:
            file.write(result + '\n')

if __name__ == "__main__":
    main()
