from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip

from .streaming import stream_camera


def index(request):
    return render(request, "streaming/index.html")


@login_required
@gzip.gzip_page
def video(request):
    return StreamingHttpResponse(
        stream_camera(),
        content_type="multipart/x-mixed-replace;boundary=frame",
    )
