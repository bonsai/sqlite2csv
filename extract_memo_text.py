import json
import csv
import re
import sys

def extract_text_from_note_json(json_file, output_file=None):
    """
    note.jsonファイルからテキスト部分のみを抽出
    日本語テキストに対応
    """
    if output_file is None:
        output_file = "memo_texts.txt"
    
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
                        # テキストには複数の\id=...行が含まれている
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
                            print(f"メモ {len(all_texts)}: {note_content}")
                
                except Exception as e:
                    continue        
        # テキストファイルに出力
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, text in enumerate(all_texts, 1):
                f.write(f"メモ {i}: {text}\n")
        
        print(f"\n✅ 抽出完了!")
        print(f"📊 抽出されたメモ数: {len(all_texts)}")
        print(f"💾 出力ファイル: {output_file}")
        
        return all_texts
        
    except FileNotFoundError:
        print(f"❌ エラー: '{json_file}'が見つかりません。")
        return []
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return []

def extract_text_to_csv(json_file, output_csv=None):
    """
    メモテキストをCSVファイルにも出力
    BOM付きUTF-8でExcel対応
    """
    if output_csv is None:
        output_csv = "memo_texts.csv"
    
    texts = extract_text_from_note_json(json_file)
    
    if texts:
        try:
            # BOM付きUTF-8でCSVファイルを作成（Excel対応）
            with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['番号', 'メモテキスト'])  # ヘッダー
                
                for i, text in enumerate(texts, 1):
                    writer.writerow([i, text])
            
            print(f"📊 CSVファイルも作成: {output_csv} (BOM付きUTF-8)")
            
        except Exception as e:
            print(f"❌ CSV出力エラー: {e}")

def extract_text_to_csv_sjis(json_file, output_csv=None):
    """
    メモテキストをShift_JIS CSVファイルに出力（古いExcel用）
    """
    if output_csv is None:
        output_csv = "memo_texts_sjis.csv"
    
    texts = extract_text_from_note_json(json_file)
    
    if texts:
        try:
            # Shift_JISでCSVファイルを作成（古いExcel対応）
            with open(output_csv, 'w', newline='', encoding='shift_jis') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['番号', 'メモテキスト'])  # ヘッダー
                
                for i, text in enumerate(texts, 1):
                    writer.writerow([i, text])
            
            print(f"📊 Shift_JIS CSVファイルも作成: {output_csv}")
            
        except UnicodeEncodeError as e:
            print(f"❌ Shift_JIS変換エラー: 一部の文字が変換できません")
            print(f"   BOM付きUTF-8版をご利用ください")
        except Exception as e:
            print(f"❌ CSV出力エラー: {e}")

def search_memo_text(json_file, search_term):
    """
    メモテキストから特定の文字列を検索
    """
    texts = extract_text_from_note_json(json_file)
    
    if not texts:
        return
    
    print(f"\n🔍 '{search_term}' を含むメモを検索中...")
    print("=" * 60)
    
    found_count = 0
    for i, text in enumerate(texts, 1):
        if search_term.lower() in text.lower():
            found_count += 1
            print(f"🎯 メモ {i}: {text}")
    
    if found_count == 0:
        print(f"'{search_term}' を含むメモは見つかりませんでした。")
    else:
        print(f"\n✅ {found_count}件のメモが見つかりました。")

def main():
    json_file = "note.json"
    
    print("🗒️  Note.json メモテキスト抽出ツール")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "search" and len(sys.argv) > 2:
            search_term = sys.argv[2]
            search_memo_text(json_file, search_term)
        elif command == "csv":
            extract_text_to_csv(json_file)
        elif command == "csv_sjis":
            extract_text_to_csv_sjis(json_file)
        else:
            print("使用方法:")
            print("  python extract_memo_text.py          # テキストファイルに出力")
            print("  python extract_memo_text.py csv      # CSVファイルに出力")
            print("  python extract_memo_text.py csv_sjis  # Shift_JIS CSVファイルに出力")
            print("  python extract_memo_text.py search 検索語  # メモを検索")
    else:
        # デフォルト: テキストファイルに出力
        extract_text_from_note_json(json_file)
        extract_text_to_csv(json_file)

if __name__ == "__main__":
    main()
