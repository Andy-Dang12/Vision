import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

"""bash
pip install Pillow pyzbar
sudo apt-get install libzbar0 libzbar-dev
"""


def create_wifi_qr(wifiname:str, password:str, show: bool=False):
    # Chuẩn bị chuỗi thông tin WiFi
    wifi_info = f"WIFI:S:{wifiname};T:WPA;P:{password};;"

    # Tạo mã QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_info)
    qr.make(fit=True)

    # Tạo ảnh và lưu
    img = qr.make_image(fill_color="black", back_color="white")

    # Hiển thị ảnh
    if show:
        img.show()

    return img


def read_qr_code(image_path):
    # Mở ảnh QR
    img = Image.open(image_path)

    # Giải mã QR code
    decoded_objects = decode(img)
    for obj in decoded_objects:
        # Trả về chuỗi thông tin đọc được từ QR
        return obj.data.decode("utf-8")

    # Trả về None nếu không tìm thấy QR code
    return None


img = create_wifi_qr("wifi_name", r"password")
img.save('wifi.png')
# Sử dụng hàm
qr_data = read_qr_code('wifi.png')
print(qr_data)
