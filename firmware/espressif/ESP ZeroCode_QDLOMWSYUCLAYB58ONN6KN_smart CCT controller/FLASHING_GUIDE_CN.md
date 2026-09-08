# ESP ZeroCode 固件烧录指南（Mac Terminal）

本文适用于当前目录中的 ESP ZeroCode Matter 灯具固件，以及使用 USB-TTL 串口连接的 ESP8684H 模组。

目标是让没有烧录经验的用户按照本文操作，完成：

1. 检查 Mac 是否识别串口；
2. 烧录公共固件镜像；
3. 烧录设备专属证书和工厂配置；
4. 读取启动日志，确认设备正常运行。

## 1. 重要结论

本项目不能只烧录 `Common binaries/all_products_merged.bin`。

完整烧录需要三个文件：

| 文件 | Flash 地址 | 作用 |
| --- | ---: | --- |
| `Common binaries/all_products_merged.bin` | `0x0` | 公共固件、Bootloader、分区表和应用 |
| `Devices/1/esp_secure_cert.bin` | `0xD000` | 设备专属 Matter 证书 |
| `Devices/1/fctry.bin` | `0x1F2000` | 设备专属工厂配置和 Matter 数据 |

设备 1 的二维码为：

```text
Devices/1/qr_code.png
```

`Devices/1` 下的两个二进制文件和二维码必须配套使用。不要把设备 1 的证书、工厂配置或二维码复制给其他设备。

## 2. 准备硬件

### 2.1 USB-TTL 接线

使用 **3.3V TTL 电平** 的 USB-TTL 转换器，连接如下：

| USB-TTL | ESP8684 模组 |
| --- | --- |
| `TXD` | 模组 `RX0` |
| `RXD` | 模组 `TX0` |
| `GND` | 模组 `GND` |

注意：

- `TXD` 和 `RXD` 必须交叉连接。
- 必须共地，否则串口可能完全没有有效通信。
- 不要使用 5V TTL。
- 如果板子已有稳定 3.3V 供电，通常只连接 `TXD`、`RXD`、`GND` 即可。
- 不要用 USB-TTL 的 5V 电源给模组供电。
- 烧录时不要同时接入其他会占用 `RX0/TX0` 的串口设备。

### 2.2 进入下载模式需要的按键

准备以下两个按键或对应测试点：

- `BOOT` / `GPIO9`：进入 UART 下载模式；
- `RST` / `EN`：复位模组。

如果板子没有标出 `BOOT`，需要将 ESP8684 的 `GPIO9` 临时拉到 `GND`，然后复位或重新上电。烧录完成后必须释放 `GPIO9`，否则设备会继续停在下载模式。

## 3. 确认文件位置

本文假定 Mac Terminal 当前目录就是本文件所在目录。先运行：

```bash
pwd
```

然后确认三个文件存在：

```bash
ls -lh \
  "Common binaries/all_products_merged.bin" \
  "Devices/1/esp_secure_cert.bin" \
  "Devices/1/fctry.bin"
```

应该看到三个文件都能列出。如果提示 `No such file or directory`，不要继续烧录，先进入正确的固件目录。

## 4. 确认 Mac 识别串口

插入 USB-TTL 后运行：

```bash
ls -l /dev/cu.*
```

当前实测端口是：

```text
/dev/cu.usbserial-14220
```

如果你的端口名称不同，后面所有命令中的 `/dev/cu.usbserial-14220` 都要替换成 Mac 实际显示的名称。

也可以直接检查当前端口：

```bash
ls -l /dev/cu.usbserial-14220
```

如果端口不存在：

1. 拔出并重新插入 USB-TTL；
2. 检查 USB-TTL 驱动是否安装；
3. 检查 USB 线是否支持数据传输；
4. 重新运行 `ls -l /dev/cu.*`。

## 5. 确认 esptool 可用

本项目实测使用 `esptool v5.3.1`。检查命令：

```bash
esptool version
```

如果提示找不到 `esptool`，可以使用本文后面所有命令中的完整路径：

```bash
/Users/apple/.local/bin/esptool version
```

如果电脑没有安装 `esptool`，安装命令为：

```bash
python3 -m pip install --user esptool
```

安装后重新打开 Terminal，再执行 `esptool version`。

## 6. 可选：先做只读连接测试

这一步不会擦除或写入 Flash，用来确认串口和下载模式正常。

运行：

```bash
esptool \
  --port /dev/cu.usbserial-14220 \
  --baud 115200 \
  --before no-reset \
  --after no-reset \
  --connect-attempts 0 \
  chip-id
```

终端会显示：

```text
Connecting....
Detecting chip type... ESP32-C2
Connected to ESP32-C2 on /dev/cu.usbserial-14220:
Chip type:          ESP8684H (revision v2.0)
Features:           Wi-Fi, BT 5 (LE), Single Core, 120MHz, Embedded Flash 4MB
```

### 6.1 看到 `Connecting...` 后怎么按键

在终端出现：

```text
Connecting....
```

立即执行：

1. 按住 `BOOT` / `GPIO9`；
2. 按一下并松开 `RST` / `EN`；
3. 继续按住 `BOOT` / `GPIO9` 约 1～2 秒；
4. 松开 `BOOT` / `GPIO9`。

如果使用测试点而不是按键：

1. 将 `GPIO9` 拉到 `GND`；
2. 给模组复位或重新上电；
3. 等待终端出现芯片识别信息；
4. 断开 `GPIO9` 到 `GND` 的连接。

成功标志是出现：

```text
Connected to ESP32-C2
Chip type: ESP8684H
```

不要把以下提示当作成功：

```text
Invalid head of packet
No serial data received
```

这些提示表示烧录器还没有和 ROM 下载程序建立连接，尚未开始写入。

## 7. 完整烧录流程

### 7.1 是否先擦除 Flash

如果这是首次烧录、设备中有旧固件、或者需要清理旧配网状态，可以先擦除：

```bash
esptool --port /dev/cu.usbserial-14220 erase-flash
```

看到以下提示后，擦除完成：

```text
Chip erase completed successfully
Hard resetting via RTS pin...
```

擦除会删除旧固件、旧 Matter 配网状态和旧分区数据。擦除后必须重新烧录三个文件。

如果只是补烧本项目的证书和工厂配置，不需要擦除，直接执行第 7.2 节即可。

### 7.2 启动烧录命令

执行下面这一条命令。它会把两个设备数据文件写入正确地址，不会擦除 `merged` 固件区：

```bash
esptool \
  --port /dev/cu.usbserial-14220 \
  --baud 115200 \
  --before no-reset \
  --after hard-reset \
  --connect-attempts 0 \
  write-flash \
  0x0 "Common binaries/all_products_merged.bin" \
  0xD000 "Devices/1/esp_secure_cert.bin" \
  0x1F2000 "Devices/1/fctry.bin"
```

### 7.3 按键时机

命令启动后，终端会出现类似：

```text
Serial port /dev/cu.usbserial-14220:
Connecting....
```

此时：

1. 按住 `BOOT` / `GPIO9`；
2. 按一下并松开 `RST` / `EN`，或者断电后重新上电；
3. 保持 `BOOT` / `GPIO9` 约 1～2 秒；
4. 松开 `BOOT` / `GPIO9`；
5. 不要拔 USB-TTL，不要关闭 Terminal，等待烧录完成。

如果自动复位线路有效，也可以不按键。但本项目实测 USB-TTL 自动复位没有稳定进入下载模式，**建议按上面的手动方式操作**。

### 7.4 连接成功后的提示

成功进入下载模式后，终端会出现：

```text
Detecting chip type... ESP32-C2
Connected to ESP32-C2 on /dev/cu.usbserial-14220:
Chip type:          ESP8684H (revision v2.0)
Features:           Wi-Fi, BT 5 (LE), Single Core, 120MHz, Embedded Flash 4MB
Crystal frequency:  26MHz
```

然后会出现：

```text
Uploading stub flasher...
Running stub flasher...
Stub flasher running.
Configuring flash size...
```

这表示已经真正连接到芯片，接下来才是写入阶段。

### 7.5 三个文件的成功提示

公共固件写入时，应看到类似：

```text
Writing 'Common binaries/all_products_merged.bin' at 0x00000000...
Wrote ... bytes ...
Verifying written data...
Hash of data verified.
```

然后是设备证书：

```text
Writing 'Devices/1/esp_secure_cert.bin' at 0x0000d000...
Flash will be erased from 0x0000d000 to 0x0000efff...
Wrote 8192 bytes ...
Verifying written data...
Hash of data verified.
```

最后是工厂配置：

```text
Writing 'Devices/1/fctry.bin' at 0x001f2000...
Flash will be erased from 0x001f2000 to 0x001f7fff...
Wrote 24576 bytes ...
Verifying written data...
Hash of data verified.
```

三个文件都出现 `Hash of data verified.` 后，才算烧录和校验完成。最后通常会看到：

```text
Hard resetting via RTS pin...
```

## 8. 烧录后查看启动日志

烧录器自动复位后，使用新的 Terminal 窗口执行：

```bash
/Users/apple/.local/share/esptool-venv/bin/python \
  -m serial.tools.miniterm \
  /dev/cu.usbserial-14220 \
  74880 \
  --raw
```

串口参数是：

```text
端口：/dev/cu.usbserial-14220
波特率：74880
数据位：8
校验位：None
停止位：1
```

启动监听后，按一下 `RST/EN` 或重新上电。正常启动应看到：

```text
ESP-ROM:esp32c2-eco4-20240515
rst:0x1 (POWERON),boot:0xc (SPI_FAST_FLASH_BOOT)
entry 0x403acb70
zero_code_product: enter main: 376 ms
light_matter: restore done: 487 ms
zero_code_utils: Chip: esp32c2
zero_code_utils: Software Version: 1.4.0
zero_code_utils: Firmware Type: Evaluation
zero_code_utils: MAC: 58:2a:bd:38:20:30
zero_code_utils: RainMaker Node ID: ...
zero_code_utils: Matter Serial Number: ...
zero_code_utils: Product Config: ...
```

当前项目的配置日志中还应能看到：

```text
"pwm_hz":4000
"gpio_cold_or_cct":5
"gpio_warm_or_brightness":4
```

退出日志监视器：

```text
Control + ]
```

也就是按住 `Control`，再按右中括号 `]`。

## 9. 如何判断烧录成功

同时满足以下条件，才算完整成功：

- 终端识别到 `ESP32-C2` / `ESP8684H`；
- 三个文件都完成写入；
- 三个文件都显示 `Hash of data verified.`；
- 最后出现 `Hard resetting via RTS pin...`；
- 重启日志显示 `boot:0xc (SPI_FAST_FLASH_BOOT)`；
- 日志中出现 `light_matter: restore done`；
- 日志中能读取 `Product Config`；
- 没有反复出现 `Getting device configuration failed: 0`。

## 10. 常见问题

### 10.1 `No serial data received`

表示烧录器没有收到芯片响应，通常是没有进入下载模式。

按以下顺序处理：

1. 关闭其他串口软件；
2. 确认 `TXD → RX0`、`RXD → TX0`、`GND → GND`；
3. 确认 USB-TTL 是 3.3V TTL；
4. 执行烧录命令，看到 `Connecting...` 后按住 `BOOT/GPIO9`；
5. 点按 `RST/EN` 或重新上电；
6. 保持 `BOOT/GPIO9` 1～2 秒后松开。

### 10.2 `Invalid head of packet`

通常表示芯片仍在正常运行并输出日志，而不是 ROM 下载模式。重新按照第 7.3 节手动进入下载模式。

### 10.3 终端出现 `waiting for download`

说明芯片已经进入下载模式，但 `esptool` 没有在正确时机连接。保持 `BOOT/GPIO9` 为低，再重新执行烧录命令；看到 `Connecting...` 后不要立即松开，直到出现 `Connected to ESP32-C2`。

### 10.4 日志是乱码

不要使用 `115200` 查看应用启动日志。当前固件实测日志波特率是 `74880`：

```bash
/Users/apple/.local/share/esptool-venv/bin/python \
  -m serial.tools.miniterm \
  /dev/cu.usbserial-14220 \
  74880 \
  --raw
```

### 10.5 `Port is busy` 或 `Operation not permitted`

关闭以下可能占用串口的程序：

- Arduino IDE 串口监视器；
- `screen`、`cu`、`miniterm`；
- 其他 Terminal 窗口中的串口监听；
- 仍在运行的 `esptool`。

检查占用进程：

```bash
lsof /dev/cu.usbserial-14220 /dev/tty.usbserial-14220
```

### 10.6 只烧录了 `merged`

如果日志出现：

```text
zero_code_core: Getting device configuration failed: 0
```

说明公共固件可以启动，但设备专属配置没有写入。重新执行第 7 节的完整烧录流程，或者至少执行：

```bash
esptool \
  --port /dev/cu.usbserial-14220 \
  --baud 115200 \
  --before no-reset \
  --after hard-reset \
  --connect-attempts 0 \
  write-flash \
  0xD000 "Devices/1/esp_secure_cert.bin" \
  0x1F2000 "Devices/1/fctry.bin"
```

## 11. 小白操作清单

按顺序逐项完成：

- [ ] USB-TTL 使用 3.3V TTL；
- [ ] `TXD → RX0`；
- [ ] `RXD → TX0`；
- [ ] `GND → GND`；
- [ ] 设备已供电；
- [ ] `ls -l /dev/cu.*` 能看到串口；
- [ ] 三个固件文件都存在；
- [ ] 执行完整 `write-flash` 命令；
- [ ] 看到 `Connecting...` 后按住 `BOOT/GPIO9`；
- [ ] 点按 `RST/EN` 或重新上电；
- [ ] 看到 `Connected to ESP32-C2` 后松开 `BOOT/GPIO9`；
- [ ] 三个文件均显示 `Hash of data verified.`；
- [ ] 看到 `Hard resetting via RTS pin...`；
- [ ] 用 `74880` 监听启动日志；
- [ ] 看到 `SPI_FAST_FLASH_BOOT`；
- [ ] 看到 `light_matter: restore done`；
- [ ] 看到 `Product Config`；
- [ ] 没有持续出现 `Getting device configuration failed: 0`。

