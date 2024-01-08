import os
import json
import base64
from datetime import datetime
from urllib.parse import urlparse

def get_netloc(url):
    """
    传入一个url获取完整的子域名
    """
    return urlparse(url).netloc if url else ''

def merge_json_files(folder_path):
    """
    将指定文件夹下的json文件合并为一个字典
    """
    indexers = {}
    for filename in os.listdir(folder_path):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict) or not data.get("domain"):
                    continue
                netloc = get_netloc(data["domain"])
                indexers[netloc] = data
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
    return indexers

def save_data_to_json(data, json_path, json_pack_path):
    """
    将数据保存为两个不同格式的json文件
    """
    version = datetime.now().strftime("%Y%m%d%H%M")
    result = {"version": version, "indexer": data}
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=True, indent=4)

    with open(json_pack_path, "w", encoding="utf-8") as f:
        json.dump(result, f, separators=(',', ':'), ensure_ascii=True)

def save_json_to_dat(json_path, bin_path):
    """
    将json文件转换为base64并保存到dat文件
    """
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = f.read()
    base64_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")
    
    with open(bin_path, "w", encoding="utf-8") as f:
        f.write(base64_data)

def format_json_file(file_path):
    """
    格式化json文件
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def format_json_files_in_folder(folder_path):
    """
    格式化指定文件夹下的所有json文件
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(".json"):
            format_json_file(file_path)

def create_or_clear_sites_file(sites_dat_path):
    """
    创建或清空文件
    """
    mode = "w" if os.path.exists(sites_dat_path) else "x"
    with open(sites_dat_path, mode):
        pass

if __name__ == "__main__":
    # 格式化sites目录下的json文件
    format_json_files_in_folder("sites")
    
    # 创建或清空相关文件
    for file_path in ["user.sites.bin", "user.sites.json", "user.sites.pack.json"]:
        create_or_clear_sites_file(file_path)
    
    # 合并json文件并保存为不同格式
    indexers = merge_json_files("sites")
    save_data_to_json(indexers, "user.sites.json", "user.sites.pack.json")
    
    # 将json文件转为dat文件
    save_json_to_dat("user.sites.pack.json", "user.sites.bin")
