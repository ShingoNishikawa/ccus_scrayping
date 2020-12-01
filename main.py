from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import csv

# スクレイピング実行処理
def RunScrayping(areaName):
    # choromeドライバーを使えるようにする。
    driver = webdriver.Chrome('chromedriver.exe')

    # ドライバーにURLを渡して開く
    driver.get('https://www.mobile.ccus.jp/#/open_jigyousya_search')

    # 開いたページから任意の要素までのXpathを指定し要素を取得、取得した要素を変数に格納
    radioElement=driver.find_element_by_xpath('/html/body/ng-component/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/span[2]/label/input')
    # 取得した要素をクリックする
    radioElement.click()
    # ページ読込の為、処理を一旦停止する
    sleep(3)

    # 開いたページから任意の要素までのXpathを指定し要素を取得、取得した要素を変数に格納
    praceElement = driver.find_element_by_xpath('/html/body/ng-component/div[2]/div/div/div[1]/div/div[2]/fieldset/div[1]/div[2]/div/select')
    # 要素をセレクトボックスエレメントに変換
    praceSelectElement = Select(praceElement)

    # セレクトボックスからエリアを選択
    praceSelectElement.select_by_visible_text(areaName)

    # ページ読込の為、処理を一旦停止する
    sleep(5)

    # 開いたページから任意の要素までのXpathを指定し要素を取得、取得した要素を変数に格納
    serchElement = driver.find_element_by_xpath('/html/body/ng-component/div[2]/div/div/div[2]/div/div/app-button[1]/button')
    # 取得した要素をクリックする
    serchElement.click()

    # ページ読込の為、処理を一旦停止する
    sleep(3)

    # 空のリストを用意する
    getData = []

    # わざと無限ループ発生させる
    while True:

        # tbody要素からtrの要素を”すべて”抽出し変数に格納する
        trElements = driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        
        # 格納した要素たちを一つずつ取り出して回す
        for trElement in trElements:
            print(trElement.text.split('\n'))
            # CSV書き込み準備を実施する　文字コードはシフトJIS、書き込みモードは追記モード
            with open('{}.csv'.format(areaName), 'a',encoding='shift_jis',newline="") as ff:
                
                # csv書き込みの為に必要なwriterを準備
                writer = csv.writer(ff)

                # writerにリストを渡して1行書き込む
                writer.writerow(trElement.text.split('\n'))
                getData.append(trElement.text.split('\n'))
        
        # 次のページへのリンクを探して取得
        nextPageLink = driver.find_element_by_class_name('pagination-next')

        if 'disabled' in nextPageLink.get_attribute("class"):
            # 次のページ要素にdisabledというクラスが設定されていたら無限ループを抜ける
            break

        print('次のPageを取得します。')
        
        # 要素をクリックする
        nextPageLink.click()
        sleep(5)

    with open('{}_bulkcreate.csv'.format(areaName), 'w',encoding='shift_jis',newline="") as f:
        writer = csv.writer(f)
        writer.writerows(getData)
    
    return


if __name__ == "__main__":
    
    # ここで取得するエリア名を事前に設定
    areas = ["京都府","滋賀県","和歌山県","兵庫県"]

    # areasリストから一つずつ取り出して関数に値を渡す。
    for area in areas:
        RunScrayping(area)