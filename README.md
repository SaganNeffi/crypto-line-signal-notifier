# 📊 Crypto RSI Signal Notifier

## 📌 專案介紹
本專案為一個以 Python 開發的加密貨幣市場監控系統，  
透過 Binance API 取得多個幣種的市場資料，並使用 RSI 技術指標判斷市場狀態，當達到設定條件時即時發送交易訊號通知至 LINE。

系統會每小時自動掃描多個交易對，並判斷是否出現超買或超賣情況，適合用於短線交易訊號監控與市場觀察。

---

## ⚙️ 使用技術
- Python
- Pandas（資料處理）
- TA-Lib（RSI 計算）
- Binance API（市場資料）
- LINE Notify API（訊號推播）

---

## 🚀 功能特色
- 📊 自動抓取 Binance 多幣種 K 線資料
- ⏱ 每小時整點自動執行
- 📈 RSI 指標判斷市場狀態
- 🔔 即時 LINE 訊號通知
- 🔄 自動更新本地資料（CSV）

---

## 🧠 訊號邏輯
- RSI ≥ 65 → 發送 SELL 訊號
- RSI ≤ 35 → 發送 BUY 訊號

👉 用於判斷市場是否處於超買或超賣區

---

## ▶️ 如何執行

### 1️⃣ 安裝套件
```bash
pip install pandas ta-lib python-binance requests
