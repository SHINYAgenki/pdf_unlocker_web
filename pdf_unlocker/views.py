from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadPDFForm
import PyPDF2
from io import BytesIO
from urllib.parse import quote  # ファイル名のエンコーディング用

def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            password = form.cleaned_data['password']
            original_filename = pdf_file.name  # アップロードされたファイルの名前を取得
            
            # ファイル名をエンコード
            encoded_filename = quote(original_filename)
            
            try:
                reader = PyPDF2.PdfReader(pdf_file)
                if reader.is_encrypted:
                    if reader.decrypt(password) == 0:
                        return HttpResponse("パスワードが間違っているか、PDFの暗号解除に失敗しました。")
                writer = PyPDF2.PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                # メモリ内でPDFを書き出す
                pdf_output = BytesIO()
                writer.write(pdf_output)
                pdf_output.seek(0)
                # レスポンスをPDFとして送信
                response = HttpResponse(pdf_output.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
                return response
            except Exception as e:
                return HttpResponse(str(e))
    else:
        form = UploadPDFForm()
    return render(request, 'pdf_unlocker/upload_pdf.html', {'form': form})
