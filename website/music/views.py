from django.shortcuts import render
import subprocess

from .models import Track, ST, Song

# Create your views here.
def index(request):
    return render(request, 'music/index.html')

def favorite(request):
    if request.method == 'POST':
        user = request.POST['user']
        recomm = request.POST['recomm']
        results = subprocess.Popen(['spark-submit', '/Users/Jacob/Desktop/Python/MSD/make_recomm.py', user, recomm], stdout=subprocess.PIPE)
        list = results.stdout.read().splitlines()[0:int(recomm)]
        l = ''
        for i in list:
            j = i.decode('utf-8')
            s = Song.objects.get(hashcode=int(j))
            st = ST.objects.get(songID=s.songID)
            try:
                t = Track.objects.get(trackID=st.trackID)
                l = l + 'Track: ' + t.name + '\t' + 'Artist: ' + t.artist + '\t' + 'Year: ' + str(t.year) + '\n'
            except Track.DoesNotExist:
                l = l + s.songID + '\n'
        context = {"results": l}
        print(results)
        return render(request, 'music/index.html', context)
    else:
        return render(request, 'music/index.html')