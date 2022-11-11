from django.shortcuts import render
import json
import requests
from bs4 import BeautifulSoup as Soup
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


def pokemon(request, number):
    pokemon_info = {}
    pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(number)).json()
    pokemon_info['types'] = get_pokemon_types(pokemon)
    pokemon_info['name'] = get_pokemon_name(pokemon)
    pokemon_info['weight'] = get_pokemon_weight(pokemon)
    pokemon_info['height'] = get_pokemon_height(pokemon)
    pokemon_info['sprite'] = get_pokemon_sprite(pokemon)
    pokemon_info['description'] = get_pokemon_description(pokemon)
    pokemon_info['title'] = get_pokemon_title(pokemon)
    context = {'pokemon_info': pokemon_info}
    return render(request, template_name='pokedex.html', context=context)


def get_pokemon_types(pokemon):
    types = pokemon["types"]
    temp = ""
    for type in types:
        type_url = type["type"]["url"]
        response = requests.get(type_url)
        data = response.json()
        for item in data["names"]:
            if item["language"]['name'] == "fr":
                temp += item['name'] + ', '
    if len(types) > 0:
        temp = temp[:-2]
    types = temp
    return types


def get_pokemon_name(pokemon):
    fr_name = None
    eng_name = pokemon["name"]  # name
    url = "https://pokeapi.co/api/v2/pokemon-species/" + eng_name
    response = requests.get(url)
    data = response.json()
    for item in data["names"]:
        if item['language']['name'] == "fr":
            fr_name = item["name"]
    return fr_name


def get_pokemon_weight(pokemon):
    lbs_weight = pokemon["weight"]
    kg_weight = ' ' + str(round(lbs_weight * 0.453592, 2)) + 'kg'
    return kg_weight


def get_pokemon_height(pokemon):
    dcm_height = pokemon["height"]
    m_height = ' ' + str(round(dcm_height / 10, 1)) + 'm'
    return m_height


def get_pokemon_sprite(pokemon):
    sprite = pokemon["sprites"]["front_default"]  # name
    return sprite


def get_pokemon_description(pokemon):
    description = None
    eng_name = pokemon["name"]  # name
    url = "https://pokeapi.co/api/v2/pokemon-species/" + eng_name
    response = requests.get(url)
    data = response.json()
    last_version = list(data["flavor_text_entries"])

    for item in data["flavor_text_entries"]:
            if item['version']['name'] == "shield" and item['language']['name'] == "fr":
                description = item["flavor_text"]
    return description

def get_pokemon_title(pokemon):
    title = None
    eng_name = pokemon["name"]  # name
    url = "https://pokeapi.co/api/v2/pokemon-species/" + eng_name
    response = requests.get(url)
    data = response.json()
    for item in data["genera"]:
        if item['language']['name'] == "fr":
            title = item["genus"]
    return title


def get_previous_path(request):
    path = request.get_full_path()
    pokemon_id = path.split('/pokedex/')[1]
    pokemon_id += -1
    path = path + str(pokemon_id)
    print(path)
    return {
       'previous_path': path
    }