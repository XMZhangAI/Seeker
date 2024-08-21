import requests
from lxml import html
import json
import os

BASE_URL = "https://docs.oracle.com/javase/8/docs/api/"

def get_tree(url):
    response = requests.get(url)
    response.raise_for_status()
    return html.fromstring(response.content)

def get_subclasses(tree):
    subclasses = []
    # 如果/html/body/div[4]/div[1]/ul/li/dl[2]/dt的文本是Direct Known Subclasses
    if len(tree.xpath('/html/body/div[4]/div[1]/ul/li/dl[2]/dt/text()')) == 0:
        return subclasses
    if tree.xpath('/html/body/div[4]/div[1]/ul/li/dl[2]/dt/text()')[0] != "Direct Known Subclasses:":
        return subclasses
    # 获取所有的Direct Known Subclasses
    dd_tags = tree.xpath('/html/body/div[4]/div[1]/ul/li/dl[2]/dd/a')
    for a_tag in dd_tags:
        subclass_name = a_tag.text
        if "Error" not in subclass_name and "Exception" not in subclass_name:
            continue
        relative_path = a_tag.get('href')
        # 把../../java/lang/中的../../去掉
        relative_path = relative_path.replace("../", "")
        absolute_url = os.path.join(os.path.dirname(BASE_URL), relative_path).replace("\\", "/")
        subclasses.append((subclass_name, absolute_url))
    return subclasses

def build_tree(class_name, url):
    tree = get_tree(url)
    print(url)
    subclasses = get_subclasses(tree)

    node = {
        "name": class_name,
        "children": []
    }

    for subclass_name, subclass_url in subclasses:
        subclass_node = build_tree(subclass_name, subclass_url)
        node["children"].append(subclass_node)

    return node

def main():
    root_class = "Throwable"
    root_url = BASE_URL + "java/lang/Throwable.html"
    tree = build_tree(root_class, root_url)

    with open("throwable_tree.json", "w", encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)

    print("Throwable class tree has been saved to throwable_tree.json")

if __name__ == "__main__":
    main()
