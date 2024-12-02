import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

def process_nfo_files(start_dir):
    for root_dir, subdirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.nfo'):
                file_path = os.path.join(root_dir, file)
                # 解析XML文件
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                except ET.ParseError:
                    print(f"Error parsing {file_path}, skipping.")
                    continue
                
                # 查找<numid>标签
                numid = root.find('.//numid')
                if numid is not None:
                    print(f"{file_path} already has <numid>, skipping.")
                    continue
                
                # 查找<uniqueid type="num">
                uniqueid_num = root.find('.//uniqueid[@type="num"]')
                if uniqueid_num is None:
                    print(f"{file_path} does not have <uniqueid type='num'>, skipping.")
                    continue
                
                # 创建<numid>标签，并添加内容
                numid_tag = ET.Element('numid')
                numid_tag.text = uniqueid_num.text
                root.append(numid_tag)
                
                # 查找<uniqueid type="cid">
                uniqueid_cid = root.find('.//uniqueid[@type="cid"]')
                if uniqueid_cid is not None:
                    cidid_tag = ET.Element('cidid')
                    cidid_tag.text = uniqueid_cid.text
                    root.append(cidid_tag)
                
                # 将XML树转换为字符串
                xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
                
                # 使用minidom格式化XML字符串
                dom = xml.dom.minidom.parseString(xml_str)
                pretty_xml = dom.toprettyxml(indent='  ')
                
                # 去除多余的空白行
                lines = [line for line in pretty_xml.splitlines() if line.strip()]
                pretty_xml = os.linesep.join(lines)
                
                # 保存格式化后的XML回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(pretty_xml)
                print(f"{file_path} processed.")

if __name__ == '__main__':
    start_dir = 'G:\\STH ERO'  # 替换为你的目标目录
    process_nfo_files(start_dir)