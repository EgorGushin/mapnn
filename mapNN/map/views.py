import folium
from django.shortcuts import render
from folium.plugins import MousePosition
import pandas as pd


def create_map(request):
    map = folium.Map([56.328348, 44.002750], zoom_start=14)
    data = pd.read_csv('map/attractions.csv')
    name = data['NAME']
    descreption = data['DESCRIPTION']
    lat = data['LAT']
    lon = data['LON']
    for name, descreption, lat, lon in zip(name, descreption, lat, lon):
        folium.Marker(
            location=[lat, lon],
            tooltip=f'<b>{name}</b>',
            popup=f'{descreption}',
            icon=folium.Icon(color='blue')
        ).add_to(map)
    mouse_position = MousePosition(
        position='topright',
        separator=' Long: ',
        empty_string='NaN',
        lng_first=False,
        num_digits=20,
        prefix='Lat:',
    )
    map.add_child(mouse_position)
    folium.Choropleth(
        geo_data='map/map.geojson',
        name='Достопримечательности'
    ).add_to(map)
    folium.LayerControl().add_to(map)
    map = map.get_root().render()
    context = {'map': map}
    return render(request, 'map.html', context)
