# Espressif ZeroCode

本文说明如何使用 ESP ZeroCode 产品。

我们假定设备 Flash 已经烧录完成，无论是通过 ZeroCode 网页门户，还是你自行烧录。如果是从下载的 zip 自行烧录，请先阅读 [固件烧录](#固件烧录)。完成后，再从本节继续。

> 注意：本固件使用的是测试证书，不能用于量产设备。下单后，ZeroCode 模组会带有正式的量产证书。

请按以下说明完成设备启动和使用。

## 配网码

使用任意支持 Matter 的手机 App（详见下文）扫描下面的二维码，即可为设备配网。

> 注意：如果自行烧录多台设备，请使用对应设备文件夹中的二维码。

<img src="https://esp-ezc-launchpad-246098634217-prod.s3.us-east-1.amazonaws.com/companies/U58UVDGJP5SFPNCCCKSDAJ/products/QDLOMWSYUCLAYB58ONN6KN/721263253_1767680254/1/qr_code.png" alt="qr_code" width="30%" />

## 设备配网

下面说明如何把本设备加入你常用的智能家居生态：

<details>
<summary>Amazon</summary>

* 前置条件：
    * Android 手机上安装最新版 Amazon Alexa App。
    * 网络中已有下列<a href="https://www.amazon.com/b?ie=UTF8&node=37490568011#:~:text=Echo%20Dot%20(5th%20Gen)%2C,(v3)%2C%20Echo%20Dot%20Gen" target="_blank">设备</a>之一完成设置：
        * Echo（至少第 4 代）
        * Echo Dot（至少第 3 代）
        * Echo Show（至少 5）
        * Echo Flex
        * Echo Input
        * Echo Plus
        * Echo Pop
        * Echo Studio
* 配网：
    * 打开 Alexa App，进入设备页。
    * 点击右上角 `+`，选择 `Add Device`。
    * 滑到最底部，选择 `Other`，再选择 `Matter`。
    * 系统会询问设备是否有 Matter 标志，选择 `Yes`。
    * 扫描二维码，或手动输入配网码。
    * 设备配网开始。
    * 按提示输入家庭网络凭据。
    * 大约一分钟后，可将设备加入房间/分组，并修改设备名称。
    * App 应显示设备已添加成功。
* 控制：
    * 可在 Alexa App 中控制设备。
    * 也可以对 `Alexa` 使用语音控制。

</details>

<details>
<summary>Apple</summary>

* 前置条件：
    * Apple 设备上安装最新版家庭 App（至少 iOS/iPadOS 16.1）。
    * 网络中已有下列<a href="https://github.com/espressif/connectedhomeip/blob/master/docs/guides/darwin.md#setup-requirements-for-application-development" target="_blank">设备</a>之一完成设置：
        * Apple HomePod（至少 tvOS 16.1）
        * Apple TV（至少 tvOS 16.1）
* 配网：
    * 打开家庭 App。
    * 点击右上角 `+`，选择 `添加配件`。
    * 扫描二维码，或手动输入配网码。
    * 设备配网开始。
    * 可能会提示正在添加 `未认证的配件`，点击 `仍然添加`。
    * 大约一分钟后，可将设备加入房间，并修改设备名称。
    * 可能会询问额外的设备设置，可以选择 `跳过` 或 `以后`。
    * App 应显示设备已添加成功。
* 控制：
    * 可在家庭 App 中控制设备。
    * 也可以对 `Siri` 使用语音控制。

</details>

<details>
<summary>Google</summary>

* 前置条件：
    * Android 手机上安装最新版 Google Home App（至少 Android 8.1）。
    * 网络中已有下列<a href="https://support.google.com/googlenest/answer/12391458" target="_blank">设备</a>之一完成设置：
        * Google Home（不支持 Thread）
        * Google Home Mini（不支持 Thread）
        * Google Nest Audio（不支持 Thread）
        * Google Nest Hub（不支持 Thread）
        * Google Nest Hub（第 2 代）
        * Google Nest Hub Max
        * Google Nest Mini（不支持 Thread）
        * Nest WiFi Pro
    * 由于本设备使用测试证书，需要先登记你的 Google 账号才能配网。可以把 Google 邮箱发给我们，我们会为该账号开通权限。
* 配网：
    * 打开 Google Home App，进入设备页。
    * 点击 `+ 添加`，选择 `新设备`。
    * 选择家庭后，App 会开始搜索附近设备。
    * 从列表中选择本设备，然后扫描二维码，或手动输入配网码。
    * 设备配网开始。
    * 大约一分钟后，App 应显示设备已添加成功。
    * 随后可将设备加入房间，并修改设备名称。
* 控制：
    * 可在 Google Home App 中控制设备。
    * 也可以对 `Google 助理` 使用语音控制。

</details>

<details>
<summary>ESP RainMaker</summary>

* 前置条件：
    * Apple 设备上安装最新版 ESP RainMaker App（至少 iOS/iPadOS 16.4）。
* 配网：
    * 打开 ESP RainMaker App，选择或创建一个分组。
    * 点击右上角 `+`。
    * 扫描二维码。
    * 可能会要求再次扫描二维码，或手动输入配网码。
    * 设备配网开始。
    * 可能会提示正在添加 `未认证的配件`，点击 `仍然添加`。
    * 大约两分钟后，App 应显示设备已添加成功。
* 控制：
    * 可在 ESP RainMaker App 中控制设备。

</details>

<details>
<summary>Samsung</summary>

* 前置条件：
    * Android 手机上安装最新版 SmartThings App。
    * 网络中已有下列<a href="https://support.smartthings.com/hc/en-us/articles/11219700390804-SmartThings-x-Matter-Integration-#" target="_blank">设备</a>之一完成设置：
        * Aeotec Smart Home Hub
        * SmartThings 2015 Hub（不支持 Thread）
        * SmartThings 2018 Hub
* 配网：
    * 打开 SmartThings App，进入设备页。
    * 点击 `+`，选择 `QR code`。
    * 扫描二维码，或手动输入配网码。
    * 设备配网开始。
    * 可能会提示这不是 Matter 认证设备，点击 `continue`。
    * 也可能会要求输入家庭网络凭据。
    * 大约一分钟后，可将设备加入房间，并修改设备名称。
    * App 应显示设备已添加成功。
* 控制：
    * 可在 SmartThings App 中控制设备。

</details>

## 设备说明

### 产品

本设备包含 1 路灯。

1. 灯：色温
    * 默认电源状态为开。
    * 上电后的电源状态与断电前相同。

### 设备驱动

本设备包含 1 路 LED。

1. LED：PWM
    * gpio_red: -1
    * gpio_green: -1
    * gpio_blue: -1
    * gpio_cold_or_cct: 5
    * gpio_warm_or_brightness: 4

## 设备功能

### 指示灯效

设备具有以下指示：

#### 配网

* **配网模式**：LED 持续白光呼吸，约 2 秒一轮。
* **配网已开始**：LED 持续白光呼吸，约 1 秒一轮。
* **配网完成**：LED 回到设备默认状态，并停止当前灯效。
* **配网失败**：LED 暖白常亮。

#### 功能


#### 测试模式


#### 识别

* **识别开始**：LED 持续白光闪烁，约 1 秒一轮。
* **识别停止**：LED 回到设备默认状态，并停止当前灯效。
* **识别闪烁**：LED 白光闪烁 1 秒，约 1 秒一轮。
* **识别呼吸**：LED 白光呼吸 15 秒，约 1 秒一轮。
* **识别正常**：LED 白光闪烁 1 秒，约 2 秒一轮。
* **识别通道切换**：LED 白光闪烁 8 秒，约 16 秒一轮。
* **识别结束效果**：LED 回到设备默认状态，并停止当前灯效。
* **识别停止效果**：LED 回到设备默认状态，并停止当前灯效。

### 恢复出厂设置

将设备恢复为出厂设置：

* 给设备断电，等待 2 秒。再上电，等待 2 秒。
* 按此方式循环断电/上电 3 次。
* 设备随后会重启并进入配网模式。

### 测试模式

面向设备制造商，固件提供测试模式，用于产线测试。设备首次启动时，会扫描附近特定的 Wi-Fi/Thread 网络，以判断要执行哪类测试动作。这些测试动作如下：

* **测试完成**：将测试模式标记为已完成。此后设备不会再进入测试模式。
    * 触发：默认（按硬件使用 Wi-Fi 或 Thread）
    * ssid: test_complete
    * panid: 0x198F
    * mac: 1212121212121212
* **BLE MAC**：通过 BLE 广播 MAC 地址。
    * 触发：默认（按硬件使用 Wi-Fi 或 Thread）
    * ssid: test_ble_mac
    * panid: 0x198F
    * mac: 3434343434343434
* **灯光 1**：灯光循环切换不同颜色。
    * 触发：默认（按硬件使用 Wi-Fi 或 Thread）
    * ssid: test_light_1
    * panid: 0x198F
    * mac: 5656565656565656
* **灯光 2**：灯光循环切换不同颜色。
    * 触发：默认（按硬件使用 Wi-Fi 或 Thread）
    * ssid: test_light_2
    * panid: 0x198F
    * mac: 7878787878787878
* **灯光 3**：灯光循环切换不同颜色。
    * 触发：默认（按硬件使用 Wi-Fi 或 Thread）
    * ssid: test_light_3
    * panid: 0x198F
    * mac: 9090909090909090

<details>
<summary>从 zip 烧录固件</summary>

## 固件烧录

如果从下载的 zip 自行烧录设备固件，请按下面对应章节操作。可以使用终端/`PowerShell` 中的 `esptool`，或使用 `Flash 下载工具`。

<details>
<summary>在命令行使用 esptool（macOS、Linux、Windows）</summary>

### 前置条件

安装 `esptool`
* 参考<a href="https://docs.espressif.com/projects/esptool/en/latest/esp32/installation.html" target="_blank">安装说明</a>
* 打开终端/`PowerShell`
* 运行：`pip install esptool`
* 连接设备并记下端口
* 下面的命令可能需要通过 `-p <port>` 指定端口

### 烧录

先擦除 Flash
* 运行：`esptool.py erase_flash`

烧录固件
* 0x0: common_binaries/*_merged.bin
* 运行：`esptool.py write_flash 0x0 common_binaries/*_merged.bin`

烧录其他必需文件
* 0xD000: devices/\<number\>/esp_secure_cert.bin
* 0x1F2000: devices/\<number\>/fctry.bin
* 运行：`esptool.py write_flash 0xD000 devices/1/esp_secure_cert.bin 0x1F2000 devices/1/fctry.bin`

设备现已就绪。可以回到 [配网码](#配网码) 一节继续设置。

</details>

<details>
<summary>使用 Flash 下载工具（Windows）</summary>

### 前置条件

安装 `Flash 下载工具`
* <a href="https://www.espressif.com/sites/default/files/tools/flash_download_tool_3.9.5.zip" target="_blank">下载</a>该工具
* 解压文件，并阅读 `doc/` 中的 PDF
* 运行 `flash_download_tool`
* 选择对应芯片后继续
* 连接设备，并在 `COM` 中选择端口

### 烧录

先擦除 Flash
* 点击 `erase`

烧录固件
* 0x0: common_binaries/*_merged.bin
* 浏览并填入该文件路径，点击 `start`

烧录其他必需文件
* 0xD000: devices/\<number\>/esp_secure_cert.bin
* 0x1F2000: devices/\<number\>/fctry.bin
* 浏览并填入这些文件路径，点击 `start`

设备现已就绪。可以回到 [配网码](#配网码) 一节继续设置。

</details>
</details>
