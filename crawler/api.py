import os
from dotenv import load_dotenv
from pathlib import Path

import google.generativeai as genai

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

GEMINI_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def extract_description(description):
    prompt = f"Ta có thông tin rao bán nhà bằng tiếng Việt như sau: \
        {description} \n \
        Hãy trích xuất thông tin trên và chuyển về csv gồm các trường thông tin dưới đây. \
        Mỗi trường thông tin ứng với 1 cột trong csv. \
        Trường nào không xuất hiện thì để là 0. \
        Danh sách các trường: num_bedroom, \
        num_diningroom, num_kitchen, num_toilet, num_floor (nếu là nhà trọ thì có mấy tầng), \
        current_floor (phòng trọ ở tầng mấy), direction (hướng nhà, 1 trong 4 giá trị Đông/Tây/Nam/Bắc), \
        street_width (số thực, theo mét). \
        Vui lòng chỉ trả lại thông tin csv, không sử dụng markdown."
        
    response = model.generate_content(prompt)

    return response.text

def extract_location(location):
    prompt = f"Ta có thông tin địa chỉ bằng tiếng Việt như sau: \
        {location} \n \
        Hãy trích xuất thông tin trên và chuyển về csv gồm các trường thông tin dưới đây. \
        Mỗi trường thông tin ứng với 1 cột trong csv. \
        Trường nào không xuất hiện thì để là rỗng. \
        Danh sách các trường: \
        street (tên đường hoặc phố. Không bao gồm ngõ/ngách. Không bao gồm số nhà ở trước tên đường. Chỉ có tên, không có chữ 'đường' ở trước), \
        ward (là phường, nhưng có thể thay bằng xã. Chỉ gồm tên, không có chữ 'phường'/'xã' ở trước), \
        district (là quận, nhưng có thể thay bằng huyện Chỉ gồm tên, không có chữ 'quận'/'huyện' ở trước). \
        Không bao gồm tên thành phố Hà Nội. \
        Vui lòng chỉ trả lại thông tin csv, không sử dụng markdown."

    response = model.generate_content(prompt)

    return response.text

# info = extract_description("Tôi cho thuê phòng trọ tầng 2 (có hai phòng 18m2, có điều hòa và bình nóng lạnh )nhà có 3 tầng. \
# Tầng có chỗ phơi quần áo riêng. giá là 1,5 triệu. \
# Khu vực gần trường Học Viện Chính Sách")

# info = extract_location("37 Hoa Bằng, Phường Yên Hòa, Quận Cầu Giấy, Hà Nội")

# print(info)