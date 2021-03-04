from vicleaners import cleaners



def main(text):
    ret = cleaners(text).do()
    print(ret)


if __name__ == '__main__':
    txt = 'Học viện Phụ nữ Việt Nam dự kiến tuyển 1000 chỉ tiêu cho 9 ngành đại học chính quy, tăng 100 chỉ tiêu so với năm ngoái. Các ngành gồm Quản trị kinh doanh, Công tác xã hội, Giới và Phát triển, Luật, Luật kinh tế, Quản trị dịch vụ du lịch và lữ hành, Kinh tế, Tâm lý học và Truyền thông đa phương tiện.'
    main(txt)