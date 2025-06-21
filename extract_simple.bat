@echo off
:: Microsoft Sticky Notes データ抽出 (簡単版)

echo Sticky Notesデータベースをコピー中...
copy "C:\Users\dance\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite" plum.sqlite

echo データベース構造を表示...
python sqlite2csv.py plum.sqlite inspect

echo 全データをCSV変換...
python sqlite2csv.py plum.sqlite export_all

echo 完了！csv_exports フォルダを確認してください
pause
