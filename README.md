### Raspberry piの基本
**初めに用意するもの<br>**
Raspberry pi 本体<br>
Rapberry pi用タッチディスプレイ<br>
Rasberry piに電源を供給するケーブル<br>
Micro SD<br>
USB付きマウス<br>
USB付きキーボード<br>

**[Micro SDなどのセットアップ](https://deviceplus.jp/hobby/raspberrypi_entry_056/
)**

**ディスプレイとの接続**<br>
* [繋ぎ方はこのページが参考になる](https://iot.nifcloud.com/blog/2015/10/26/raspberry-pi-display/)
* 繋ぎ方の図↓
<img src="./images/how_to_connect.jpg">

**Raspberry pi3　ピンの位置**<br>
<img width="300" src="./images/raspi_pin.png">
<br>

**インストール編**
* matplotlib<br>
  * python3なら`$ pip3 install matplotlib`<br>
  * python2なら`$ sudo apt-get install python-matplotlib --fix-missing`


### Raspberry piとMacを接続
* まずアプリをインストール :
[アプリのURL](https://www.realvnc.com/en/connect/download/viewer/)
* 実行するコード<br>
<Raspberry pi側の操作>
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
Wi-fiに繋がっていることを確認してから
```
$ sudo apt-get install tightvncserver
$ tightvncserver　（パスワード設定）
```
<Mac側の操作><br>
  * アプリの立ち上げ<br>
  * ウィンドウにラズパイのIPアドレスを打ち込む
  * 先ほど指定したパスワードを入れる<br>
  ＊IPアドレスはこれ
  <img width="500" src="./images/ip_address.jpg"><br>
  ＊ディスプレイ番号が必要なので要注意<br>
  <img width="500" src="./images/raspi_mac.jpg"><br>   
<br>

### 加速度センサ　MM8452Q
* 繋ぎ方↓<br>
<img width="400" src="./images/accl_sensor.png">


#### 加速度検出　\~エラー解決編~
**case 1**<br>
bus=smbus.SMBus(1)<br>
[Error] No such file or directory<br>

 **解決法**<br>
Raspberry piのターミナルに<br>
`$raspi-config`
を打ち込んで出てきた画面で<br>
5 Interfacing Options ▶︎ P5 I2C ▶︎ <はい＞の順に選択。<br>
リブートしてやり直す。<br>

**case 2**<br>
I/O error<br>
▶︎ センサとの接続がうまく言っていないときにおこるエラー<br>
　 まず以下をRaspberry piのターミナルに打ち込んでみる。<br>
`$ i2cdetect -y 1`<br>

 ▶︎ 全てが`--`になっているとき<br>
センサとの接続が出来ていない。抑えながらやったり、回路を組み直したり、電源を抜いてやり直したりしてみる。<br>
▶︎`--`でない箇所があるとき<br>
何かしらの文字（○○とする）が入っている部分がセンサからの入力がきている部分なので、自分の書いたプログラムで　I2C_ADDR=0x○○　が正しく記入されているかを確認する。

### フルカラーシリアルLEDテープ
[このページに載っているGitHubのコードをダウンロード！](http://jellyware.jp/kurage/raspi/led_stick.html)<br>
ロジック変換しないでもいけてしまった...。<br>
上記サイトの"回路結線図"以降を参照。
strandtest.pyの中身を応用すれば良さそう！加速度の結果とどう結びつけるかは後日検討。<br>
<img width="200" src="./images/led_rainbow.jpg">


### スピーカー　CY-ET805D
* まだ接続出来てません...。<br>
  おそらくこのスピーカーなのだけどネットで調べると修理のページしか出てこない。安直に5VとGNDに繋げば良いのだろうか？<br>
  [このスピーカー？？](https://minkara.carview.co.jp/userid/539393/car/2388612/4410054/note.aspx)<br>

  [Raspberry pi 出力先の変更](https://iot-plus.net/make/raspi/speaker-open-jtalk-japanese-speech/)<br>
  [pygameでmp3再生](https://qiita.com/week/items/ab190474eeb7c1fe9fc2)<br>

* 330Ω抵抗一つ挟んでスピーカーを接続してみたら、Raspberry pi の画面が消えた。ちょっと危険かも？<br>

▶︎ USBタイプのスピーカーを使ったほうが楽かも...。<br>
