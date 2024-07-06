from django.shortcuts import render,HttpResponse,redirect
from pytube import YouTube
from django.http import FileResponse
from django.conf import settings
import os


def download(request):
    content ={
        'title': 'Youtube Video Download',
        'heading': 'Download',
    }
    return render(request, 'download.html',content)

def process_video(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')
        if not youtube_url:
            context = {
                'title': 'Welcome to My Website',
                'description': 'This is a sample Django project.',
                'error': 'YouTube URL field cannot be empty.',
            }
            return render(request, 'download.html', context)
        
        yt = YouTube(youtube_url)
        thumbail_url = yt.thumbnail_url
        videos = yt.streams.filter(progressive=True, file_extension='mp4').desc()
        # videos = yt.streams.filter(subtype = 'mp4').order_by('resolution').desc()
        formate =[]
        for stream in videos:
            formate.append({'itag': stream.itag, 'resolution': stream.resolution, 'mime_type': stream.mime_type})

        video_info ={
            'thumbnail_url' : thumbail_url,
            'youtube_url': youtube_url,
            'title': yt.title,
            'duration':str(yt.length // 60) + ':' + str(yt.length % 60),
            'formats':formate
        }


        context = {
           
            'video_info': video_info,
        }
     
        return render(request, 'download.html', context)
    return redirect('download')


def download_video(request,youtube_url,itag):
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.get_by_itag(itag)
        file_path =video.download(output_path=settings.MEDIA_ROOT)

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    except Exception as e:
        return HttpResponse(str(e))
