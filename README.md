# AI Trader Pro 全自動版

功能：
- Telegram 自動推播
- Bitget 行情
- BTC / ETH / XAUUSDT / CLUSDT
- RSI / EMA / MACD / ATR / 支撐壓力
- 新聞 RSS 掃描與市場情緒摘要
- 每 5 分鐘自動戰情室
- 每日 06:00、21:00 固定戰情室
- Railway / Docker 可部署

## 使用方法

1. 解壓縮
2. 複製 `.env.example` 成 `.env`
3. 填入新的 Telegram Token 與 Bitget API
4. 安裝：

```bash
python -m pip install -r requirements.txt
```

5. 執行：

```bash
python main.py
```

## Railway

Procfile 已內建：

```text
worker: python main.py
```

把專案推到 GitHub，Railway 連接 Repo，Variables 填入 `.env` 的內容即可。

## 安全提醒

你之前貼出的 API Key / Secret / Telegram Token 已經外洩，務必刪除重建。

## 自動下單

預設 `ENABLE_AUTO_TRADE=false`，本版只推播不下單，避免程式一啟動就用真金白銀下單。
