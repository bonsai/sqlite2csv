import sqlite3
import csv
import os
import sys
import json
import re
from datetime import datetime

def inspect_database(db_file):
    """
    SQLiteデータベースの構造を表示
    """
    if not os.path.exists(db_file):
        print(f"❌ エラー: '{db_file}'が見つかりません。")
        return []
    
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str  # 文字化け対策
        cursor = conn.cursor()
        
        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("データベースにテーブルが見つかりませんでした。")
            return []
        
        print(f"📊 データベース '{db_file}' のテーブル一覧:")
        print("=" * 60)
        
        table_names = []
        for table in tables:
            table_name = table[0]
            table_names.append(table_name)
            print(f"\n📋 テーブル: {table_name}")
            
            # テーブルの構造を取得
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("   カラム構造:")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = "PRIMARY KEY" if col[5] else ""
                not_null = "NOT NULL" if col[3] else ""
                print(f"     - {col_name} ({col_type}) {is_pk} {not_null}")
            
            # レコード数を取得
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   📊 レコード数: {count}")
        
        conn.close()
        return table_names
        
    except sqlite3.Error as e:
        print(f"❌ SQLiteエラー: {e}")
        return []
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return []

def export_table_to_csv(db_file, table_name, output_csv=None, encoding='utf-8-sig'):
    """
    指定したテーブルをCSVにエクスポート
    """
    if output_csv is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"{table_name}_{timestamp}.csv"
    
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str  # 文字化け対策
        cursor = conn.cursor()
        
        # テーブルのデータを取得
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # カラム名を取得
        column_names = [description[0] for description in cursor.description]
        
        if not rows:
            print(f"⚠️  テーブル '{table_name}' にデータがありません。")
            conn.close()
            return False
        
        # CSVに出力
        with open(output_csv, 'w', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  # ヘッダー
            writer.writerows(rows)
        
        conn.close()
        
        print(f"✅ テーブル '{table_name}' をCSVにエクスポートしました")
        print(f"💾 出力ファイル: {output_csv}")
        print(f"📊 レコード数: {len(rows)}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLiteエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def export_all_tables(db_file, output_dir=None, encoding='utf-8-sig'):
    """
    すべてのテーブルをCSVにエクスポート
    """
    if output_dir is None:
        output_dir = "csv_exports"
    
    # 出力ディレクトリを作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 出力ディレクトリを作成: {output_dir}")
    
    tables = inspect_database(db_file)
    if not tables:
        return
    
    print(f"\n🔄 すべてのテーブルをCSVにエクスポート中...")
    print("=" * 60)
    
    success_count = 0
    for table_name in tables:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = os.path.join(output_dir, f"{table_name}_{timestamp}.csv")
        
        if export_table_to_csv(db_file, table_name, output_csv, encoding):
            success_count += 1
        print()
    
    print(f"🎉 完了: {success_count}/{len(tables)} テーブルをエクスポートしました")

def extract_text_columns(db_file, table_name, text_columns=None, output_csv=None):
    """
    テーブルからテキストカラムのみを抽出してCSVに出力
    """
    if output_csv is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"{table_name}_text_{timestamp}.csv"
    
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
        cursor = conn.cursor()
        
        # テーブル構造を取得
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        
        # テキスト系のカラムを自動検出
        if text_columns is None:
            text_columns = []
            for col in columns_info:
                col_name = col[1]
                col_type = col[2].upper()
                if any(text_type in col_type for text_type in ['TEXT', 'VARCHAR', 'CHAR', 'CLOB']):
                    text_columns.append(col_name)
        
        if not text_columns:
            print(f"⚠️  テーブル '{table_name}' にテキストカラムが見つかりません。")
            conn.close()
            return False
        
        print(f"📝 抽出するテキストカラム: {', '.join(text_columns)}")
        
        # 指定したカラムのデータを取得
        columns_str = ', '.join(f'"{col}"' for col in text_columns)
        cursor.execute(f"SELECT {columns_str} FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"⚠️  テーブル '{table_name}' にデータがありません。")
            conn.close()
            return False
        
        # CSVに出力
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(text_columns)  # ヘッダー
            writer.writerows(rows)
        
        conn.close()
        
        print(f"✅ テキストカラムをCSVにエクスポートしました")
        print(f"💾 出力ファイル: {output_csv}")
        print(f"📊 レコード数: {len(rows)}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLiteエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def search_text_in_database(db_file, search_term, tables=None):
    """
    データベース内のテキストを検索
    """
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
        cursor = conn.cursor()
        
        if tables is None:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
        
        print(f"🔍 '{search_term}' を検索中...")
        print("=" * 60)
        
        total_found = 0
        
        for table_name in tables:
            # テーブル構造を取得
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            
            # テキスト系のカラムを検索
            text_columns = []
            for col in columns_info:
                col_name = col[1]
                col_type = col[2].upper()
                if any(text_type in col_type for text_type in ['TEXT', 'VARCHAR', 'CHAR', 'CLOB']):
                    text_columns.append(col_name)
            
            if not text_columns:
                continue
            
            # 各テキストカラムで検索
            found_in_table = 0
            for col_name in text_columns:
                cursor.execute(f'SELECT * FROM {table_name} WHERE "{col_name}" LIKE ?', 
                             (f'%{search_term}%',))
                results = cursor.fetchall()
                
                if results:
                    found_in_table += len(results)
                    print(f"📋 テーブル '{table_name}', カラム '{col_name}': {len(results)}件")
                    
                    # 最初の3件を表示
                    for i, row in enumerate(results[:3], 1):
                        print(f"   {i}. {row}")
                    
                    if len(results) > 3:
                        print(f"   ... 他 {len(results) - 3}件")
            
            if found_in_table > 0:
                total_found += found_in_table
                print()
        
        conn.close()
        
        if total_found == 0:
            print(f"'{search_term}' を含むデータは見つかりませんでした。")
        else:
            print(f"✅ 合計 {total_found}件のデータが見つかりました。")
        
    except sqlite3.Error as e:
        print(f"❌ SQLiteエラー: {e}")
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")

def main():
    print("🗃️  SQLite to CSV 変換ツール")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python sqlite2csv.py <database.db> [command] [options]")
        print()
        print("コマンド:")
        print("  inspect                     # データベース構造を表示")
        print("  export <table_name>         # 指定テーブルをCSVにエクスポート")
        print("  export_all                  # すべてのテーブルをCSVにエクスポート")
        print("  text <table_name>           # テキストカラムのみ抽出")
        print("  search <search_term>        # データベース内を検索")
        print()
        print("例:")
        print("  python sqlite2csv.py plum.sqlite inspect")
        print("  python sqlite2csv.py plum.sqlite export User")
        print("  python sqlite2csv.py plum.sqlite export_all")
        print("  python sqlite2csv.py plum.sqlite text notes")
        print("  python sqlite2csv.py plum.sqlite search 'cssマスター'")
        return
    
    db_file = sys.argv[1]
    
    if not os.path.exists(db_file):
        print(f"❌ エラー: データベースファイル '{db_file}' が見つかりません。")
        return
    
    if len(sys.argv) == 2:
        # デフォルト: データベース構造を表示
        inspect_database(db_file)
        return
    
    command = sys.argv[2]
    
    if command == "inspect":
        inspect_database(db_file)
    
    elif command == "export" and len(sys.argv) > 3:
        table_name = sys.argv[3]
        export_table_to_csv(db_file, table_name)
    
    elif command == "export_all":
        export_all_tables(db_file)
    
    elif command == "text" and len(sys.argv) > 3:
        table_name = sys.argv[3]
        extract_text_columns(db_file, table_name)
    
    elif command == "search" and len(sys.argv) > 3:
        search_term = sys.argv[3]
        search_text_in_database(db_file, search_term)
    
    else:
        print("❌ 無効なコマンドです。使用方法を確認してください。")

if __name__ == "__main__":
    main()
