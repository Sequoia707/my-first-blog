from django.shortcuts import render

# Create your views here.

def PostListView(request):
	return render(request, 'blogone/home.html')