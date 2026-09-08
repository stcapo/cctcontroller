# 项目第一需求
  硬件部分设计见firmware/schmatic
  固件由乐鑫zerocode platform 生成测试固件 
  ## 一句话定义

  开发一款可量产并面向欧洲销售的 12–24V DC Matter 双路双色温灯带控制器，由内部 MOSFET 直接驱动冷白/暖白灯带，可通过 Apple Home、Google Home 和 Amazon Alexa 控制开关、亮度和色温。

  ## 产品边界

  - 产品类型：双色温 CCT 灯带控制器，不是完整灯具。
  - 供电输入：12–24V DC。
  - 销售包装：只卖控制器，不附带 230V 电源适配器。
  - 负载输出：直接输出：
      - LED+
      - CW- 冷白
      - WW- 暖白
  - 功率结构：内部双路 MOSFET 直接控制灯带电流。
  - 无线方案：ESP8684-mini-1，Matter over Wi‑Fi，蓝牙用于首次配网。
  - 目标市场：欧洲。
  - 当前未确定项：单路最大电流、总功率、端子规格和最终外壳尺寸。

  ## 核心功能

  用户在智能家居平台中应能完成：

  1. 扫描二维码完成 Matter 配网；
  2. 开灯、关灯；
  3. 调节整体亮度；
  4. 调节冷暖色温；
  5. 在最暖端主要点亮暖白通道；
  6. 在最冷端主要点亮冷白通道；
  7. 关闭时两个 MOSFET 通道都必须可靠关断；
  8. 断电重启后恢复到产品规定的状态。

  目标生态：

  - Apple Home——当前样机已经接入成功；
  - Google Home；
  - Amazon Alexa；
  - 后续通过 Matter Multi-Admin 加入多个生态。

  ## 当前 ZeroCode 配置

  见图 zerocode_config.png
  当前正式加载到样机中的配置是：

  芯片：ESP8684-mini-1 (Zerocode平台上配置的是esp8684-wroom-03, 已验证, 功能完全适配mini-1 所以选用mini-1)
  模式：Lighting Fixture
  控制：Brightness + Temperature
  Temperature Mode：CCT/Brightness
  PWM 频率：4000 Hz
  GPIO5：Cold / CCT
  GPIO4：Warm / Brightness
  色温范围：2200K–7000K

  但目前只能确认软件成功加载了这些参数，还需要通过 PCB 走线、示波器和真实灯带确认：

  GPIO5 → 冷白 MOSFET Gate → CW-
  GPIO4 → 暖白 MOSFET Gate → WW-

  这是当前最重要的硬件验证门槛。

  ## 第一需求验收标准

  第一需求完成必须同时满足：

  ### 1. 基础功能

  - Apple Home 可以正常配网；
  - 开关、亮度、色温控制正常；
  - 暖冷方向正确；
  - PWM 频率实测约 4000 Hz；
  - 关闭时两路输出均为零；
  - 不出现闪烁、通道反向或无法完全关灯。

  ### 2. 硬件输出

  - GPIO4/GPIO5 与两路 MOSFET 的连接正确；
  - MOSFET 高低电平逻辑正确；
  - CW- 和 WW- 不接反；
  - 12V 和24V 输入均能稳定工作；
  - 最大额定负载下端子、PCB、MOSFET不过热；
  - 具备必要的反接、短路、过流和浪涌保护。

  ### 3. Matter 量产

  - 每台设备具有唯一 Matter DAC/证书；
  - 每台设备具有唯一序列号和二维码；
  - 二维码、证书和设备数据能够一一对应；
  - 工厂烧录后能够自动校验；
  - 测试凭证不能复制到量产设备；
  - 当前 Firmware Type: Evaluation 必须替换为正式量产固件与正式凭证。

  ### 4. 欧洲销售

  - 完成最终外壳和标签；
  - 完成 CE/RED、EMC、RoHS 等测试；
  - 建立 WEEE、GPSR、产品追溯和欧盟责任人资料；
  - 准备说明书、风险分析、技术文件和 EU Declaration of Conformity；
  - 产品说明明确要求使用符合规格的 12–24V DC SELV 电源。

  ## 当前明确不做

  第一阶段不包含：

  - 230V 市电直接输入；
  - 随产品附带电源适配器；
  - RGB 彩色灯带；
  - 自建手机 App；
  - 自建云服务；
  - Thread；
  - 语音音箱硬件；
  - 旧 T3-3S/Tuya 固件路线。

  ## 当前项目阶段

  概念配置          已完成
  ZeroCode 固件生成  已完成
  固件烧录          已完成
  设备专属数据烧录  已完成
  Apple Home 配网    已完成
  GPIO/MOSFET 实测   待完成
  电流与功率定义     待完成
  保护电路验证       待完成
  外壳设计           待完成
  量产 Matter 凭证   待完成
  欧洲合规认证       待完成