#data functions
import geopandas as gpd

def prepare_geodataframes(stations_df: pd.DataFrame, counties_gdf: gpd.GeoDataFrame):
    """
    Prepares the stations and counties GeoDataFrames.
    - Creates point geometries for stations.
    - Converts stations DataFrame to GeoDataFrame.
    - Reprojects counties GeoDataFrame to EPSG:4326.

    Args:
        stations_df (pd.DataFrame): Original stations DataFrame with 'lon' and 'lat'.
        counties_gdf (gpd.GeoDataFrame): Original counties GeoDataFrame.

    Returns:
        tuple: (stations_gdf, counties_gdf) as prepared GeoDataFrames.
    """
    # Create point geometry for stations
    stations_df['points'] = gpd.points_from_xy(stations_df.lon, stations_df.lat)
    stations_gdf = gpd.GeoDataFrame(data=stations_df, geometry='points')

    # Reproject counties GeoDataFrame
    counties_gdf = counties_gdf.to_crs('EPSG:4326')
    
    return stations_gdf, counties_gdf

def perform_spatial_join(stations_gdf: gpd.GeoDataFrame, counties_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Performs a spatial join between stations and counties GeoDataFrames.

    Args:
        stations_gdf (gpd.GeoDataFrame): Prepared stations GeoDataFrame.
        counties_gdf (gpd.GeoDataFrame): Prepared counties GeoDataFrame.

    Returns:
        gpd.GeoDataFrame: The result of the spatial join (full_df).
    """
    # Perform spatial join
    full_df = gpd.sjoin(left_df=stations_gdf, right_df=counties_gdf, how='left')
    return full_df
