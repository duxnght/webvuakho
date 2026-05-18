from django.shortcuts import render
from django.http import JsonResponse

def home_page(request):
    # Khớp với file home.html mà bạn đang đặt trong thư mục templates
    return render(request, 'home.html')

def tai_lieu_page(request):
    # Tạo tạm để không bị lỗi, bạn có thể tạo trang tai_lieu.html thực sự sau
    return render(request, 'home.html') 

def dang_ky_tu_van(request):
    # Xử lý form AJAX gửi số điện thoại, tạm thời trả về thông báo thành công
    return JsonResponse({'status': 'success', 'message': 'Đăng ký thành công'})
def danh_muc_du_an(request):
    # Nếu bạn có model DuAn, có thể query ở đây: list_du_an = DuAn.objects.all()
    return render(request, 'danh_muc_du_an.html')