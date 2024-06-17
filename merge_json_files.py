import json

def merge_json_files(file1, file2, file3, output_file):
    def load_json(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)

    data1 = load_json(file1)
    data2 = load_json(file2)
    data3 = load_json(file3)

    combined_data = data1 + data2 + data3

    merged_data = {}
    for entry in combined_data:
        title = entry["title"]
        if title in merged_data:
            for key, value in entry.items():
                if key not in merged_data[title] or not merged_data[title][key]:
                    merged_data[title][key] = value
        else:
            merged_data[title] = entry

    merged_list = list(merged_data.values())

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)

