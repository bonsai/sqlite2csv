import json
import csv
import re
import sys
from datetime import datetime

def create_memo_csv_fixed():
    """
    文字化け対策済みのCSVファイルを新しい名前で作成
    """
    json_file = "note.json"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"memo_texts_{timestamp}.csv"
    
    try:
        # CSVファイルとして読み込み
        with open(json_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # ヘッダー行をスキップ
            
            all_texts = []
            
            print(f"📝 {json_file} からメモテキストを抽出中...")
            print("=" * 60)
            
            for row_num, row in enumerate(csv_reader, 1):
                try:
                    if len(row) > 0:
                        # 最初のカラム（Text）からメモテキストを抽出
                        text_column = row[0]
                        
                        # \id=...形式のテキストを抽出
                        lines = text_column.split('\n')
                        memo_texts = []
                        
                        for line in lines:
                            line = line.strip()
                            if line.startswith('\\id='):
                                # \id=xxxxx テキスト の形式からテキスト部分を抽出
                                parts = line.split(' ', 1)
                                if len(parts) > 1:
                                    memo_text = parts[1].strip()
                                    if memo_text:  # 空でないテキストのみ
                                        memo_texts.append(memo_text)
                        
                        if memo_texts:
                            note_content = ' | '.join(memo_texts)
                            all_texts.append(note_content)
                            print(f"メモ {len(all_texts)}: {note_content[:50]}...")
                
                except Exception as e:
                    continue
        
        # BOM付きUTF-8でCSVファイルを作成
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['番号', 'メモテキスト'])  # ヘッダー
            
            for i, text in enumerate(all_texts, 1):
                writer.writerow([i, text])
        
        print(f"\n✅ 抽出完了!")
        print(f"📊 抽出されたメモ数: {len(all_texts)}")
        print(f"💾 BOM付きUTF-8 CSVファイル: {output_csv}")
        print(f"📌 このファイルはExcelで文字化けせずに開けます")
        
        return output_csv
        
    except FileNotFoundError:
        print(f"❌ エラー: '{json_file}'が見つかりません。")
        return None
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return None

if __name__ == "__main__":
    print("🗒️  文字化け対策版 メモテキスト抽出ツール")
    print("=" * 60)
    create_memo_csv_fixed()
