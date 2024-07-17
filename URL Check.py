import os
import sys
import requests
from datetime import datetime
from alive_progress import alive_bar

# 顯示版本資訊
def show_version_info():
    print("====================================================================================")
    print("=                                                                                  =")
    print("=                                 URL_Check v1.0.0                                 =")
    print("=                                                                       By. Chek   =")
    print("====================================================================================")
    print()

# 檢查網址
def check_urls(urls):
    results = {}
    with alive_bar(len(urls), title='檢查網址: ') as bar:
        for url in urls:
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                if response.status_code == 200:
                    results[url] = '正常'
                else:
                    results[url] = f'無效 ({response.status_code})'
            except requests.RequestException as e:
                results[url] = f'無效 (錯誤: {e})'
            bar()  # 更新進度條
    return results

# 統計記錄檔
def save_results_to_file(results, filename):
    valid_urls = {url: status for url, status in results.items() if '正常' in status}
    invalid_urls = {url: status for url, status in results.items() if '無效' in status}
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'總網址數量: {len(results)}\n')
        file.write(f'正常網址數: {len(valid_urls)}\n')
        file.write(f'無效網址數: {len(invalid_urls)}\n\n')

        file.write('正常網址:\n')
        for url in valid_urls:
            file.write(f'{url}\n')

        file.write('\n無效網址:\n')
        for url, status in invalid_urls.items():
            file.write(f'{url} : {status}\n')

# 從 TXT 讀取網址列表
def read_urls_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls


# 程式版本
show_version_info()

# 檢查 URL.txt 是否存在，若不存在則建立
urls_file = 'URL.txt'
if not os.path.exists(urls_file):
    print(f'警告: 文件 {urls_file} 不存在，已建立請輸入資料。')
    
    with open(urls_file, 'w', encoding='utf-8') as file:
        pass  # 建立空白文件

    print()
    os.system('pause')
    sys.exit()

# 從 TXT 讀取網址列表
urls = read_urls_from_file(urls_file)

if not urls:
    print(f'警告: 文件 {urls_file} 為空。請在文件中添加要檢查的網址。')
    print()
else:
    # 批量查詢網址
    results = check_urls(urls)

    # 生成結果文件名
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = 'Log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    results_file = os.path.join(log_dir, f'URL_Check-{timestamp}.txt')
    
    # 將結果記錄到文件
    save_results_to_file(results, results_file)

    # 顯示結果統計
    total_urls = len(results)
    valid_count = len([status for status in results.values() if '正常' in status])
    invalid_count = len([status for status in results.values() if '無效' in status])

    # 少於 10個則顯示結果
    if total_urls < 10:
        print()
        for url, status in results.items():
            print(f'{url}: {status}')

    print()
    print('------------------------------------------------------------------------------------')
    print(f'總網址數量: {total_urls}')
    print(f'正常網址數: {valid_count}')
    print(f'無效網址數: {invalid_count}')
    print('------------------------------------------------------------------------------------')

print()
os.system('pause')
sys.exit()
