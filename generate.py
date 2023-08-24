import os
import json
import base64
from urllib.parse import urlparse

def format_json_file(file_path):
    """
    格式化json文件
    """
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {file_path}: {e}")
            return

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def format_json_files_in_folder(folder_path):
    """
    格式化sites目录下的json文件
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(".json"):
            format_json_file(file_path)

def create_or_clear_sites_file(sites_dat_path):
    """
    创建或清空文件
    """
    if os.path.exists(sites_dat_path):
        with open(sites_dat_path, "w") as f:
            f.truncate(0)
    else:
        with open(sites_dat_path, "w") as f:
            pass

def read_and_base64_to_sites_file(folder_path, sites_dat_path):
    """
    遍历文件夹并将文件内容转换为 base64 追加到 sites.dat 中
    """
    if not os.path.exists(sites_dat_path):
        print("sites.dat 文件不存在，请先创建或指定正确的路径")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                file_content = f.read()
                encoded_content = base64.b64encode(file_content.encode()).decode()
                with open(sites_dat_path, "a") as sites_file:
                    sites_file.write(encoded_content + "\n")
            print(f"文件 {filename} 内容已添加到 sites.dat")

def decode_base64_to_json(base64_string):
    """
    base64转换为json字符串
    """
    try:
        decoded_bytes = base64.b64decode(base64_string)
        decoded_json = decoded_bytes.decode("utf-8")
        return decoded_json
    except Exception as e:
        print(f"Error decoding base64 string: {e}")
        return None

def convert_base64_line_to_json(line_number):
    """
    base64文件，输入任意行号转换json字符串
    """
    file_path = "sites.dat"
    with open(file_path, "r") as f:
        lines = f.readlines()

    if 0 <= line_number < len(lines):
        base64_string = lines[line_number].strip()
        decoded_json = decode_base64_to_json(base64_string)
        if decoded_json:
            try:
                json_data = json.loads(decoded_json)
                json_str = json.dumps(json_data, indent=4)
            except json.JSONDecodeError as e:
                return f"Error decoding JSON: {e}"
        else:
            return "Failed to decode base64 string."
    else:
        return "Invalid line number."

def decode_base64_to_dict(base64_string):
    """
    base64字符串转换json字典
    """
    try:
        decoded_bytes = base64.b64decode(base64_string)
        decoded_json = decoded_bytes.decode("utf-8")
        return json.loads(decoded_json)
    except Exception as e:
        print(f"Error decoding base64 string: {e}")
        return None

def convert_base64_to_sites_file(sites_dat_path, sites_json_path):
    """
    将文件转换为json
    """
    result = []
    with open(sites_dat_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            base64_string = line.strip()
            decoded_dict = decode_base64_to_dict(base64_string)
            if decoded_dict:
                result.append(decoded_dict)
    if result:
        result_str = json.dumps(result, indent=4)
        with open(sites_json_path, "a") as sites_file:
            sites_file.write(result_str)

if __name__ == "__main__":
    format_json_files_in_folder("sites")
    create_or_clear_sites_file("sites.dat")
    read_and_base64_to_sites_file("sites", "sites.dat")

    # 仅用来校对
    # create_or_clear_sites_file("sites.json")
    # convert_base64_to_sites_file("sites.dat", "sites.json")