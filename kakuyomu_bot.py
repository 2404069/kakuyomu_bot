import time
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1565226717306552383/PwInbihnTHBFxLwCAiiu92eu3JtoX1Zb9rJjHKSmt05kenMVf-KkMKFQ0JZG9K0UfsXb"

TARGET_NOVELS = [
    {
        "url": "https://kakuyomu.jp/works/11054822664612029006",
        "last_title": "13.合格者たちの討伐任務"  
    },
    {
        "url": "https://kakuyomu.jp/works/822139840943828128",
        "last_title": "1-30『エピローグ／三度目の目覚め』" 
    },
    {
        "url": "https://kakuyomu.jp/works/2912051602624199029",
        "last_title": "第142話 悪役貴族、聖女に覚悟を問う" 
    },
    {
        "url": "https://kakuyomu.jp/works/11054822663060044455",
        "last_title": "第52話 日帰りできるくらいの距離が一番疲れる" 
    },
    {
        "url": "https://kakuyomu.jp/works/2912051606854917513",
        "last_title": "しずえ様の味と匂いも感じたい！" 
    },
    {
        "url": "https://kakuyomu.jp/works/2912051596979356676",
        "last_title": "顔がキモいって言われた（つらい）" 
    },
    {
        "url": "https://kakuyomu.jp/works/11054822662712553068",
        "last_title": "第37話" 
    },  
    {
        "url": "https://kakuyomu.jp/works/11054822663814504924",
        "last_title": "第23話 ほっかむりの王女" 
    },  
    {
        "url": "https://kakuyomu.jp/works/2912051605963241331",
        "last_title": "第52話 新たな出会い" 
    },                       
]

def check_kakuyomu_updates():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonBot/1.0"
    }
    
    for novel in TARGET_NOVELS:
        url = novel["url"]
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"アクセス失敗 ({url}): ステータスコード {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            episode_elements = soup.select("a[href*='/episodes/']")
            
            if not episode_elements:
                print(f"エピソードが見つかりませんでした: {url}")
                continue

            current_episode_title = episode_elements[-1].get_text(strip=True)
            
            if novel["last_title"] == "":
                novel["last_title"] = current_episode_title
                print(f"【初期化】{current_episode_title}")
                continue

            if current_episode_title != novel["last_title"]:
                message = f"📚 **カクヨム更新通知！**\n新しい話が投稿されました！\n> **{current_episode_title}**\n<{url}>"
                send_discord_notification(message)
                novel["last_title"] = current_episode_title
            else:
                print(f"更新なし: {current_episode_title}")

        except Exception as e:
            print(f"エラー発生 ({url}): {e}")
        
        time.sleep(2)

def send_discord_notification(message: str):
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code in [200, 204]:
            print("Discordへ通知を送信しました！")
        else:
            print(f"Discord通知失敗: ステータスコード {response.status_code}")
    except Exception as e:
        print(f"Discord通知の送信に失敗: {e}")

if __name__ == "__main__":
    print("複数作品のカクヨム更新チェックボットを起動しました...")
    
    while True:
        check_kakuyomu_updates()
        print("--- チェック完了。次の巡回まで待機します ---")
        time.sleep(180) 