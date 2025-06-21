@echo off
echo SQLite2CSV - Microsoft Sticky Notes データ抽出ツール
echo ================================================

:: Sticky Notesデータベースのパス
set SOURCE_DB="C:\Users\dance\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite"
set TARGET_DB="plum.sqlite"

echo.
echo 1. Sticky Notesデータベースをコピー中...
if exist %SOURCE_DB% (
    copy %SOURCE_DB% %TARGET_DB%
    if %ERRORLEVEL% EQU 0 (
        echo ✓ データベースのコピーが完了しました: %TARGET_DB%
    ) else (
        echo ✗ データベースのコピーに失敗しました
        pause
        exit /b 1
    )
) else (
    echo ✗ Sticky Notesデータベースが見つかりません: %SOURCE_DB%
    echo   Sticky Notesアプリを起動してメモを作成してから再実行してください
    pause
    exit /b 1
)

echo.
echo 2. データベース構造を確認中...
python sqlite2csv.py %TARGET_DB% inspect

echo.
echo 3. 全テーブルをCSVに変換中...
python sqlite2csv.py %TARGET_DB% export_all

echo.
echo 4. テキストデータのみを抽出中...
echo   注: テーブル名は上記の構造確認結果を参考にしてください
echo   一般的なテーブル名: Note, User, SyncState など

echo.
echo ================================================
echo 抽出完了！csv_exports/ フォルダを確認してください
echo.
echo 使用可能なコマンド:
echo   特定テーブルの抽出: python sqlite2csv.py %TARGET_DB% export テーブル名
echo   テキストのみ抽出:   python sqlite2csv.py %TARGET_DB% text テーブル名
echo   データ検索:         python sqlite2csv.py %TARGET_DB% search "検索語"
echo ================================================
pause
