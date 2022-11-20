from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt

from pokedex.models import Pokemon, Equipe


# Create your views here.


# def pokedex(request):
#     pokemons = requests.get("https://pokeapi.co/api/v2/pokemon?limit=251").json()
#     test = get_pokemons_fr(pokemons)
#     context = {'pokemons': pokemons, 'test': test}
#     return render(request, template_name='pokedex.html', context=context)


def pokemon(request, number):
    pokemon_info = {}
    path_info = {}
    pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(number))

    if pokemon:
        pokemon = pokemon.json()
    else:
        return JsonResponse({"success": "false", "message": "Le pokémon n'existe pas"}, status=400)

    pokemon_info['types'] = get_pokemon_types(pokemon)
    pokemon_info['name'] = get_pokemon_name(pokemon)
    pokemon_info['weight'] = get_pokemon_weight(pokemon)
    pokemon_info['height'] = get_pokemon_height(pokemon)
    pokemon_info['sprites'] = get_pokemon_sprites(pokemon)
    pokemon_info['description'] = get_pokemon_description(pokemon)
    pokemon_info['title'] = get_pokemon_title(pokemon)
    pokemon_info['team'] = get_pokedex_team()
    paths = get_paths(request)

    path_info['previous'] = paths[0]
    path_info['next'] = paths[1]
    context = {'pokemon_info': pokemon_info, 'path_info': path_info}
    return render(request, template_name='pokedex.html', context=context)


@csrf_exempt
def add_to_equipe(request, team_id):
    pokemon_id = request.POST.get("pokemonId")

    try:
        equipe = Equipe.objects.get(name=str(team_id))
    except Equipe.DoesNotExist:
        equipe = Equipe(name=str(team_id))
        equipe.save()

    if len(equipe.pokemons.filter(api_id=pokemon_id)) > 0:
        return JsonResponse({"success": "false", "message": "Le pokémon est déjà dans l'équipe"}, status=400)

    pokemons_team = equipe.pokemons.all()
    if len(pokemons_team) >= 6:
        return JsonResponse({"success": "false", "message": "L'équipe est déjà pleine"}, status=400)

    pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon_id).json()
    img_default = get_animated_sprite(pokemon)

    pokemon = Pokemon(api_id=pokemon_id, img=img_default)
    pokemon.save()

    equipe.pokemons.add(pokemon)

    return JsonResponse({"success": "true", "pokemon": model_to_dict(pokemon)})


@csrf_exempt
def delete_from_equipe(request, team_id, pokemon_id):
    try:
        equipe = Equipe.objects.get(name=str(team_id))
    except Equipe.DoesNotExist:
        return JsonResponse({"success": "false"}, status=404)

    pokemon = Pokemon.objects.get(api_id=pokemon_id)
    equipe.pokemons.remove(pokemon)

    Pokemon.objects.get(api_id=pokemon_id).delete()

    return JsonResponse({"success": "true"})


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


def get_animated_sprite(pokemon):
    animated_sprite = pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"]
    return animated_sprite


def get_animated_sprite_shiny(pokemon):
    return pokemon["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_shiny"]


def get_pokedex_team():
    pokedex_team_images = [{}, {}, {}, {}, {}, {}]
    try:
        equipe = Equipe.objects.get(name=1)
        pokedex_team = equipe.pokemons.all()

        for pokemon in pokedex_team:
            pokedex_team_images.insert(0, {
                "pokemon_id": pokemon.api_id,
                "pokemon_image": pokemon.img
            })
            del pokedex_team_images[-1]
        return pokedex_team_images

    except Equipe.DoesNotExist:
        return pokedex_team_images
