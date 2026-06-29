#visualization helpers
def create_base_map(center_coords=[-1.34, 37.5], zoom=5):
    """
    Initializes and returns a basic Folium map.
    """
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
    attr = 'Tiles &copy; Esri — Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
    map_obj = folium.Map(location=center_coords, zoom_start=zoom, tiles=tiles, attr=attr)
    return map_obj

def add_station_markers(map_obj, full_df, icon_path):
    """
    Adds station markers to the given map object.
    """
    weather_station_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(25, 25))
    for _, row in full_df.iterrows():
        location = [row['lat'], row['lon']]
        popup = f"{row['Station']} station {row['rainfall']}mm received"
        folium.Marker(location=location, popup=popup, icon=weather_station_icon).add_to(map_obj)
    return map_obj

################################################
def add_choropleth_layer_with_tooltip(map_obj,
                                      geo_data,
                                      data,
                                      columns,
                                      key_on,
                                      fill_color,
                                      legend_name,
                                      tooltip_fields,
                                      tooltip_aliases,
                                      popup_fields=None,
                                      popup_aliases=None):
    """
    Adds a choropleth layer and an interactive GeoJson layer with tooltips and optional popups to the map.

    Args:
        map_obj (folium.Map): The Folium map object to add layers to.
        geo_data (GeoDataFrame or GeoJSON dict/str): The geographical data for the choropleth and tooltips.
        data (pd.DataFrame): The data containing values for coloring and tooltips.
        columns (list): List of [key_column, value_column] for choropleth coloring.
        key_on (str): GeoJSON property key to join on (e.g., 'feature.properties.COUNTIES').
        fill_color (str): Color scheme for the choropleth (e.g., 'OrRd', 'PuBu').
        legend_name (str): Name for the choropleth legend.
        tooltip_fields (list): List of column names to show in the tooltip.
        tooltip_aliases (list): List of aliases for the tooltip fields.
        popup_fields (list, optional): List of column names to show in the popup. Defaults to None.
        popup_aliases (list, optional): List of aliases for the popup fields. Defaults to None.

    Returns:
        folium.Map: The updated Folium map object.
    """

    # Add the choropleth layer for coloring
    folium.Choropleth(
        geo_data=geo_data.to_json(), # Convert GeoDataFrame to GeoJSON string for folium
        data=data,
        key_on=key_on,
        columns=columns,
        fill_color=fill_color,
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name=legend_name
    ).add_to(map_obj)

    # Create a separate GeoJson layer for interactive tooltips/popups
    # This layer is transparent and uses the same geo_data
    geojson_interactive_layer = folium.GeoJson(
        geo_data, # Pass GeoDataFrame directly
        name=f'{legend_name} Interactive Layer',
        style_function=lambda x: {
            'fillColor': '#ffffff',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0 # Make it transparent
        }
    )

    # Add the tooltip as a child to the GeoJson layer
    geojson_interactive_layer.add_child(
        folium.features.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            labels=True
        )
    )

    # Add the popup as a child to the GeoJson layer if fields are provided
    if popup_fields and popup_aliases:
        geojson_interactive_layer.add_child(
            folium.features.GeoJsonPopup(
                fields=popup_fields,
                aliases=popup_aliases,
                labels=True
            )
        )

    geojson_interactive_layer.add_to(map_obj)
    return map_obj
