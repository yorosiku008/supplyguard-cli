# SupplyGuard JP

[![Tests](https://github.com/yorosiku008/supplyguard-cli/actions/workflows/test.yml/badge.svg)](https://github.com/yorosiku008/supplyguard-cli/actions)

サプライチェーンセキュリティ評価CLI — SBOM/CVE・アンケート・インシデント履歴の3軸でベンダーリスクを定量評価します。EU CRA・経産省ガイドライン対応。

## インストール

```bash
git clone https://github.com/yorosiku008/supplyguard-cli.git
cd supplyguard-cli
pip install -r requirements.txt
```

## 使い方

```bash
# デモデータで動作確認（3社比較、外部API不要）
python main.py --demo

# Markdownレポートも保存
python main.py --demo --output-md
```

## スコアリング軸

| 軸 | 重み | 評価内容 |
|---|---|---|
| SBOM / CVE | 45% | SBOMの有無 / CRITICAL・HIGH CVE件数 |
| アンケート | 35% | セキュリティアンケートの回答率・適合率 |
| インシデント履歴 | 20% | 直近12ヶ月のインシデント件数・侵害履歴 |

**グレード:** S(90+) / A(80+) / B(70+) / C(60+) / D(50+) / E(0+)

## デモ出力例

```
ベンダー名              グレード  スコア  SBOM/CVE  アンケート  インシデント
Alpha製造株式会社       B         76      55        89         100
Beta Systems Ltd.       S         96      90        100        100
Gamma Tech Partners     D         56      70        52         30
```

## テスト

```bash
pytest tests/ -v
# 22 passed
```

## EU CRA対応

- SBOM未提出でスコア大幅減点（2027年施行予定のEU Cyber Resilience Act準拠）
- CRITICAL CVEは1件あたり25点減点
- インシデント報告義務違反（侵害履歴）は40点減点

---

*SupplyGuard JP v0.1.0 — β版ユーザー募集中: yorosiku008@gmail.com*
