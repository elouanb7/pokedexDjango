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
    path_info = {}
    pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(number)).json()
    pokemon_info['types'] = get_pokemon_types(pokemon)
    pokemon_info['name'] = get_pokemon_name(pokemon)
    pokemon_info['weight'] = get_pokemon_weight(pokemon)
    pokemon_info['height'] = get_pokemon_height(pokemon)
    pokemon_info['sprites'] = get_pokemon_sprites(pokemon)
    pokemon_info['description'] = get_pokemon_description(pokemon)
    pokemon_info['title'] = get_pokemon_title(pokemon)
    paths = get_paths(request)

    path_info['previous'] = paths[0]
    path_info['next'] = paths[1]
    context = {'pokemon_info': pokemon_info, 'path_info': path_info}
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
    hecg_weight = pokemon["weight"]
    kg_weight = ' ' + str(round(hecg_weight / 10, 1)) + 'kg'
    # kg_weight = ' ' + str(round(lbs_weight * 0.453592, 2)) + 'kg'
    return kg_weight


def get_pokemon_height(pokemon):
    dcm_height = pokemon["height"]
    m_height = ' ' + str(round(dcm_height / 10, 1)) + 'm'
    return m_height


def get_pokemon_sprites(pokemon):
    pokemon_sprites = {'sprite_front_default': pokemon["sprites"]["front_default"],
                       'sprite_back_default': pokemon["sprites"]["back_default"],
                       'sprite_front_shiny': pokemon["sprites"]["front_shiny"],
                       'sprite_back_shiny': pokemon["sprites"]["back_shiny"],
                       'sprite_female_front_shiny': pokemon["sprites"]["front_shiny_female"],
                       'sprite_female_back_shiny': pokemon["sprites"]["back_shiny_female"],
                       'sprite_female_front': pokemon["sprites"]["front_female"],
                       'sprite_female_back': pokemon["sprites"]["back_female"],
                       }
    return pokemon_sprites


def get_pokemon_description(pokemon):
    description = None
    eng_name = pokemon["name"]  # name
    url = "https://pokeapi.co/api/v2/pokemon-species/" + eng_name
    response = requests.get(url)
    data = response.json()
    entries = list(data["flavor_text_entries"])
    last_version = entries[len(entries) - 2]['version']['name']
    for item in data["flavor_text_entries"]:
        if item['version']['name'] == last_version and item['language']['name'] == "fr":
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


def get_paths(request):
    path = request.get_full_path()
    pokemon_id = int(path.split('/pokedex/')[1])
    splited_path = path.split(str(pokemon_id))[0]
    if pokemon_id > 1:
        previous_path = splited_path + str(pokemon_id - 1)
    else:
        previous_path = splited_path + str(pokemon_id)
    if pokemon_id < 251:
        next_path = splited_path + str(pokemon_id + 1)
    else:
        next_path = splited_path + str(pokemon_id)
    return previous_path, next_path


def get_user_input(request):
    # path_user_input = get_user_input(request)
    path = request.get_full_path()
    pokemon_id = int(path.split('/pokedex/')[1])
    splited_path = path.split(str(pokemon_id))[0]
    path = splited_path + str(request.GET.get("inputText"))
    print(path)
    return path
