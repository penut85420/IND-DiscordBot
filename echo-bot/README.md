# First Echo Bot
+ Echo Bot
    + 你說蝦米，他就回你蝦米
        ![](https://i.imgur.com/sS8eexo.png)
+ 建立 Discord Bot Client
    ```python=
    import discord
    
    client = discord.Client()
    ```
+ 建立 `on_ready` 事件：
    + `on_ready` 會在 Bot 成功與 Discord 連上線時呼叫。
    + 透過這個事件來對 Bot 進行初始化。
    + 此步驟可用來提醒開發端是否有成功連線。
        ```python=4
        @client.event
        async def on_ready():
            print('Ready!')
        ```
    + 印出一個簡單的訊息來表示連線成功。
+ 建立 `on_message` 事件：
    + `on_message` 事件會在 Bot 接收到任何人的訊息時被呼叫。
    + 核心指令功能都會透過這個事件作為溝通橋梁。
        ```python=7
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            await message.channel.send(message.content)
        ```
    + 先判斷發送訊息的人不是機器人本人，不然就會一直 Echo 自己的 Echo。
        ![](https://i.imgur.com/GOFneaN.png)
    + `message.content` 為使用者發送出來的訊息。
    + 使用 `message.channel.send` 來發送訊息。
+ 建立啟動機器人的主函式：
    ```python=13
    if __name__ == '__main__':
        token = os.environ['TOKEN']
        client.run(token)
    ```
    + 使用 `pipenv` 執行時，會將 `.env` 裡的變數放入環境變數。
    + 使用 `os.environ` 可以存取環境變數。
+ [完整程式碼](https://git.io/JffNW)

## Reference
+ [discord.py - A Minimal Bot](https://tinyurl.com/y7cwkj2y)
+ [discord.py - discord.Message](https://tinyurl.com/y4ofczgw)
+ [Python 3's f-Strings](https://realpython.com/python-f-strings/)