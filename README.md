# RP2040_HID
RaspiPicoをHIDデバイス化するファームウェアとサンプルコードです。

Mycropythonベースのファームウェア 
firmware.uf2
をRaspiPicoに入れれば使用できます。

## Thonnyに接続する方法
GPIO21をGNDに接続した状態でPCと接続してください。

##　起動する方法
GPIO21を開放状態かプルアップした接続で電源を入れてください。

## ライブラリ
boot.py　に以下のコードを追加して初期化してください。

import hid
hid.hid_init()

#main.py　などに以下のコードを追加してください。
import hid
x_axis = 1
y_axis = 10f
z_axis = 10
rx_axis = 127
ry_axis = 0
rz_axis = -100

hid.send_hid_report(int(x_axis),int(y_axis),int(z_axis),int(rx_axis),int(ry_axis),int(rz_axis),1)
#hid.send_hid_report()のaxisパラメータは-127~127の範囲でご使用できます。

# unityとの互換性について
Input System1.4.2で動作確認済
Unityで以下の操作を行うことでHID deviceの状態を見れます。
Window -> Analysis -> Input debugger -> mysterisou-garage HID Device

## 確認されている不具合
unityへ入力される値が127を超える場合、符号bitが1となるため、負の値になります。
Mycropython上で調整いただくか、unityのHIDキー設定を書き換える必要があります。
Mycropython上で調整についてはサンプルプログラムを参照ください。

##　サポート
バグや不具合等ありましたら、以下の連絡先までご連絡お願いします。
mail:
hiropon@mysterious-garage.com

# Author
name:    hiropon2gou
circle:  mysterious-garage.com
## License
* MIT
