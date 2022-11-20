"""myDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.pokedex, name="pokedex"),
    path('<int:number>', views.pokemon, name="pokemon"),
    path('equipe/<int:team_id>', views.add_to_equipe, name="add_to_equipe"),
    path('equipe/<int:team_id>/<int:pokemon_id>', views.delete_from_equipe, name='delete_from_equipe'),
]