from django.shortcuts import render
from django.http import JsonResponse

def home_page(request):
    # Khớp với file home.html mà bạn đang đặt trong thư mục templates
    return render(request, 'home.html')

def tai_lieu_page(request):
    # Trỏ chính xác đến file tailieu.html đã được tạo
    return render(request, 'tailieu.html') 

def dang_ky_tu_van(request):
    # Xử lý form AJAX, tạm thời trả về thông báo thành công
    return JsonResponse({'status': 'success', 'message': 'Đăng ký thành công'})

def danh_muc_du_an(request):
    # Nếu bạn có model DuAn, có thể query ở đây: list_du_an = DuAn.objects.all()
    return render(request, 'danh_muc_du_an.html')
def blog_page(request):
    # Tạm thời trả về template trắng (sẽ hiển thị data mẫu 'Sắp ra mắt'). 
    # Sau này có database thì query posts truyền vào context sau.
    return render(request, 'blog.html')
def blog_page(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog_detail.html')