# F.M.T (First Meeting Topic)

<p align="center">
<img src="https://github.com/carlos-paniagua/KB_1903/blob/master/FMT%E3%83%AD%E3%82%B4.png" alt="ロゴ" width="1000">
</p>
<a href=https://www.youtube.com/watch?v=tcBbgtV4f2M><img src=https://img.youtube.com/vi/tcBbgtV4f2M/0.jpg></a>
---

### 製品概要
## __communication X Tech__

### 背景
* 授業等で初対面の人たちとチームを組む際に話のネタが思いつかない...
* 一部の人しか盛り上がらない話より、チーム全体で盛り上がる話がわからない...
* 相手の趣味とか興味があることから話のネタを提供してくれる存在がいたら助かるのでは？
という点からコミュニケーションが苦手な人やコミュニケーションを促進したいチームリーダーの人が使えるものを作ってみました
---

### 製品説明
話のネタが思いつかない？グループトークが盛りが上がらない？
それなら __F.M.T(First Meeting Topic)__ をお使いください!
LINEBotがグループの趣味を自動的に分析し、最適な話のネタを __提供__ してくれます!
さらに、自分の趣味が記載された __電子名刺__ を自動作成!
__F.M.Tで最高のLINEトーク&名刺交換を楽しみましょう!__　　

<p align="center">
<img src="https://github.com/carlos-paniagua/KB_1903/blob/master/%E8%A7%A3%E8%AA%AC11.png" alt="解説1" width="400"> <img src="https://github.com/carlos-paniagua/KB_1903/blob/master/%E8%A7%A3%E8%AA%AC2.png" alt="解説2" width="400">
</p>



---

### 特長
LINEで上記の課題を解決できるように作成しました
利用方法はあらかじめ趣味や興味をあることを記入しておくだけ！
あとは、グループにbotを招待し、合い言葉を言うと事前に集めたデータからそのグループで盛り上がりそうなものを紹介してくれます！
####  1. 特長1　記入したデータは他人には見られません
他人の目が気になるような人でも他人に入力したデータをみられないので安心！
####  2. 特長2　みんなが会話できる内容をできるかぎり探してくれます
入力内容からできるだけ一致する内容を探します
####  3. 特長3
初対面の人との会話が弾むよう趣味が記載した電子名刺を作成
パソコン,スマホに対応させました

<p align="center">
<img src="https://github.com/carlos-paniagua/KB_1903/blob/master/%E5%90%8D%E5%88%BApc.png" alt="名刺pc" width="400">    <img src="https://github.com/carlos-paniagua/KB_1903/blob/master/%E5%90%8D%E5%88%BAsmart.png" alt="名刺smart" width="300">
</p>
<p>
　　　　　　　　　　　　　　名刺パソコン版           　　　　　　　　　　　　　　　名刺スマホ版
</p>

---

### 解決出来ること
グループ上や現実での会話が促進され、より強固なチームワークの構築に一役買ってくれるはず！

---

### 今後の展望

twitterと連携し高性能かつ正確なLINEBot,電子名刺をを作成する
文脈解析の精度を上げそれぞれのユーザーの関心、興味などをユーザーの実態にそうように発展させる

---

## 開発内容・開発技術
### 活用した技術

#### API
* Docomo 固有表現抽出API

#### フレームワーク・ライブラリ・モジュール
* requests
* pickle
* re
* random

### 独自開発技術
#### 2日間に開発した独自の機能・技術
構文解析アルゴリズム、データベース、興味関心をもつ共通の話題を検出する統計学的アルゴリズム
対話によりBotがtwitterと連携の実装
