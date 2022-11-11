from django.shortcuts import render
import json
import requests
import pprint as pp


# Create your views here.
def index(request):
    context = {'test': "test"}
    return render(request, template_name='index.html', context=context)


# def pokedex(request):
#     pokemons = requests.get("https://pokeapi.co/api/v2/pokemon?limit=251").json()
#     test = get_pokemons_fr(pokemons)
#     context = {'pokemons': pokemons, 'test': test}
#     return render(request, template_name='pokedex.html', context=context)


def get_pokemons_fr(pokemons):
    pokemons_names = {'results': []}
    for pokemon in pokemons["results"]:
        # name_or_id = 1  # id
        name_or_id = pokemon["name"]  # name
        url = "https://pokeapi.co/api/v2/pokemon-species/" + name_or_id
        response = requests.get(url)
        data = response.json()
        for item in data["names"]:
            if item['language']['name'] == "fr":
                pokemons_names["results"].append(item["name"])
    return pokemons_names


def pokemon(request, number):
    pokemon_info = {}
    pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(number)).json()
    pokemon_info['types'] = pokemon_types(pokemon)
    pokemon_info['name'] = pokemon["name"]
    context = {'pokemon_info': pokemon_info}
    return render(request, template_name='pokedex.html', context=context)


def pokemon_types(pokemons):
    types = pokemons["types"]
    temp = ""
    for type in types:
        type_url = type["type"]["url"]
        response = requests.get(type_url)
        data = response.json()
        print(data)
        for item in data["names"]:
            if item["language"]['name'] == "fr":
                temp += item['name'] + ', '
    if len(types) > 0:
        temp = temp[:-2]
    types = temp
    return types
