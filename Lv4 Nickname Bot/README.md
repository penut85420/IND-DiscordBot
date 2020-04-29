# Nickname Monitor

## 簡介
+ 檢查使用者的暱稱是否符合指定的格式，來改變使用者的身分組。

## 用法
+ `!register [channel] [right_role] [wrong_role] [nickname_format]`
    + `channel` 為發布訊息的頻道，使用者的身分組有任何變動時會在這個頻道公告。
    + `right_role` 為暱稱設定正確時的身分組。
    + `wrong_role` 為暱稱設定錯誤時的身分組。
    + `nickname_format` 為暱稱格式，使用正規表示式。
+ 使用範例：
    + `!register #公告 @大神 @凡人 \[\w+\]*`