from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'titi': "j'ai cru voir un beau minou"}
    return render(request, template_name='index.html', context=context)


def pokedex(request):
    return render(request, template_name='pokedex.html')
