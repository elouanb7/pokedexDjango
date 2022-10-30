from django.shortcuts import render
import requests
import json
import requests
import pprint as pp


# Create your views here.
def index(request):
    context = {'titi': "j'ai cru voir un beau minou"}
    return render(request, template_name='index.html', context=context)


def pokedex(request):
    pokemons = requests.get("https://pokeapi.co/api/v2/pokemon?limit=251").json()
    test = get_pokemons_fr(pokemons)
    context = {'pokemons': pokemons, 'test': test}
    return render(request, template_name='pokedex.html', context=context)


def get_pokemons_fr(pokemons):
    pokemons_names = {'results': []}
    for pokemon in pokemons["results"]:
        # name_or_id = 1  # id
        name_or_id = pokemon["name"] #name
        url = "https://pokeapi.co/api/v2/pokemon-species/"+name_or_id
        response = requests.get(url)
        data = response.json()
        for item in data["names"]:
            if item['language']['name'] == "fr":
                pokemons_names["results"].append(item["name"])
    return pokemons_names
