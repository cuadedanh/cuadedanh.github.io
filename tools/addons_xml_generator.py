import os
import hashlib

class Generator:
    """ Tự động quét các thư mục addon để tạo file addons.xml và addons.xml.md5 """
    def __init__(self):
        # Đường dẫn gốc của repo (nơi chứa các folder addon)
        self.output_path = "."
        self._generate_addons_xml()
        self._generate_md5()
        print("--- Đã cập nhật xong addons.xml và mã MD5 ---")

    def _generate_addons_xml(self):
        # Khởi tạo nội dung file XML tổng
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        
        # Duyệt qua từng thư mục trong repo
        for folder in os.listdir(self.output_path):
            xml_path = os.path.join(self.output_path, folder, "addon.xml")
            
            # Chỉ xử lý nếu đó là thư mục và có chứa file addon.xml bên trong
            if os.path.isdir(os.path.join(self.output_path, folder)) and os.path.exists(xml_path):
                try:
                    with open(xml_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Loại bỏ các dòng khai báo XML thừa để gộp vào file chung
                        content = content.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
                        content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
                        addons_xml += content.strip() + "\n"
                    print(f"Đã thêm: {folder}")
                except Exception as e:
                    print(f"Lỗi khi đọc {folder}: {e}")

        addons_xml += u"</addons>\n"
        
        # Ghi nội dung ra file addons.xml ở thư mục gốc của Repo B
        with open(os.path.join(self.output_path, "addons.xml"), "w", encoding="utf-8") as f:
            f.write(addons_xml)

    def _generate_md5(self):
        # Tạo mã MD5 để Kodi biết khi nào có sự thay đổi
        with open(os.path.join(self.output_path, "addons.xml"), "rb") as f:
            m = hashlib.md5(f.read()).hexdigest()
        
        with open(os.path.join(self.output_path, "addons.xml.md5"), "w") as f:
            f.write(m)

if __name__ == "__main__":
    Generator()
