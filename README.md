# SQLite to CSV Converter

SQLiteデータベースからCSVファイルへの変換を行う日本語対応ツールです。

## 🚀 特徴

- **日本語完全対応** - UTF-8エンコーディングで文字化け防止
- **BOM付きUTF-8出力** - Excelで直接開ける日本語CSVファイル
- **柔軟なデータ抽出** - テーブル全体またはテキストカラムのみ抽出可能
- **強力な検索機能** - データベース内の文字列検索
- **詳細なデータベース解析** - テーブル構造とデータ型の詳細表示
- **エラーハンドリング** - 空のテーブルやエラーに対する適切な処理
## � インストール

```bash
git clone https://github.com/yourusername/sqlite-to-csv-converter.git
cd sqlite-to-csv-converter
```

必要な依存関係：
- Python 3.6+
- 標準ライブラリのみ（追加パッケージ不要）

## 🛠️ 使用方法

### 基本的な使い方

```bash
# データベース構造を表示
python sqlite2csv.py database.db inspect

# 特定テーブルをCSVにエクスポート
python sqlite2csv.py database.db export table_name

# すべてのテーブルをCSVにエクスポート
python sqlite2csv.py database.db export_all

# テキストカラムのみを抽出
python sqlite2csv.py database.db text table_name

# データベース内を検索
python sqlite2csv.py database.db search "検索語"
```

### コマンド詳細

| コマンド | 説明 | 例 |
|----------|------|-----|
| `inspect` | データベースの構造を表示 | `python sqlite2csv.py data.db inspect` |
| `export <table>` | 指定テーブルをCSVに変換 | `python sqlite2csv.py data.db export users` |
| `export_all` | 全テーブルを一括でCSV変換 | `python sqlite2csv.py data.db export_all` |
| `text <table>` | テキストカラムのみ抽出 | `python sqlite2csv.py data.db text notes` |
| `search <term>` | データベース内文字列検索 | `python sqlite2csv.py data.db search "keyword"` |

## 📊 出力形式

- **エンコーディング**: BOM付きUTF-8（Excel対応）
- **ファイル名**: `テーブル名_YYYYMMDD_HHMMSS.csv`
- **出力先**: 
  - 単体エクスポート: カレントディレクトリ
  - 一括エクスポート: `csv_exports/` フォルダ

## 💡 使用例

### 例1: データベースの内容確認
```bash
python sqlite2csv.py sample.db inspect
```

### 例2: メモアプリのデータ抽出
```bash
# メモのテキスト部分のみ抽出
python sqlite2csv.py notes.db text Note

# "重要"というキーワードを含むメモを検索
python sqlite2csv.py notes.db search "重要"
```

### 例3: 全データのバックアップ
```bash
# すべてのテーブルをCSVでバックアップ
python sqlite2csv.py backup.db export_all
```

## 🏗️ プロジェクト構造

```
sqlite-to-csv-converter/
├── sqlite2csv.py          # メインスクリプト
├── extract_memo_text.py   # メモテキスト抽出専用ツール
├── extract_memo_fixed.py  # 文字化け対策版
├── README.md              # このファイル
├── requirements.txt       # 依存関係
└── csv_exports/          # CSV出力ディレクトリ（自動作成）
```

## 🔧 技術詳細

### 対応データ型
- **TEXT**, **VARCHAR**, **CHAR**, **CLOB** - テキスト系データとして処理
- **INTEGER**, **REAL**, **NUMERIC** - 数値データ
- **BLOB** - バイナリデータ（そのまま出力）

### 文字化け対策
- データベース読み込み時: `conn.text_factory = str`
- CSV出力時: `encoding='utf-8-sig'` (BOM付きUTF-8)

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📈 バージョン履歴

### v1.0.0 (2025-06-22)
- 初回リリース
- 基本的なCSV変換機能
- 日本語文字化け対策
- データベース検索機能
- テキストカラム抽出機能
- SQLiteファイルが破損していないことを確認
