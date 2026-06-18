import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from ckeditor_uploader.utils import get_media_url, storage
from ckeditor_uploader.views import get_upload_filename

from .image_utils import to_webp


class WebpImageUploadView(generic.View):
    """Nhận ảnh từ CKEditor (dán/kéo-thả/tab Tải lên), chuyển sang WebP rồi lưu
    qua storage mặc định (Cloudinary trên production) — giống pipeline ảnh đại diện."""

    http_method_names = ["post"]

    def post(self, request, **kwargs):
        uploaded_file = request.FILES["upload"]

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        webp = to_webp(uploaded_file)
        if webp is None:
            message = "Tệp tải lên không phải ảnh hợp lệ."
            if ck_func_num:
                return HttpResponse(
                    "<script>window.parent.CKEDITOR.tools.callFunction(%s, '', '%s');</script>"
                    % (ck_func_num, message)
                )
            return JsonResponse({"uploaded": 0, "error": {"message": message}})

        filepath = get_upload_filename(webp.name, request)
        saved_path = storage.save(filepath, webp)
        url = get_media_url(saved_path)

        if ck_func_num:
            return HttpResponse(
                "<script>window.parent.CKEDITOR.tools.callFunction(%s, '%s');</script>"
                % (ck_func_num, url)
            )

        _, filename = os.path.split(saved_path)
        return JsonResponse({"url": url, "uploaded": "1", "fileName": filename})


upload = csrf_exempt(staff_member_required(WebpImageUploadView.as_view()))
