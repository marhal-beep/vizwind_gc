# General
from dataclasses import dataclass
import pandas as pd
import numpy as np
import turf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dash_table, html
import plotly.express as px
import random
from random import sample

pd.options.mode.chained_assignment = None  # default='warn'

# from helpfile import *
# from flask_caching import Cache# Dash
import dash
import dash_daq as daq
from dash import Dash, dcc,  Input, Output, State, callback_context, ctx
from dash.dependencies import ClientsideFunction, Input, Output
import dash_bootstrap_components as dbc
# For Map Visualization
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
# import * as L from 'leaflet';
# import { Map, MapOptions, MarkerClusterGroup, MarkerClusterGroupOptions } from 'leaflet';
# import 'leaflet.markercluster';

# def zoom_center(lons, lats):
#     # """Finds optimal zoom and centering for a plotly mapbox.
#     # Must be passed (lons & lats) or lonlats.
#     # Temporary solution awaiting official implementation, see:
#     # https://github.com/plotly/plotly.js/issues/3434
    
#     # Parameters
#     # --------
#     # lons: tuple, optional, longitude component of each location
#     # lats: tuple, optional, latitude component of each location
#     # lonlats: tuple, optional, gps locations
#     # format: str, specifying the order of longitud and latitude dimensions,
#     #     expected values: 'lonlat' or 'latlon', only used if passed lonlats
#     # projection: str, only accepting 'mercator' at the moment,
#     #     raises `NotImplementedError` if other is passed
#     # width_to_height: float, expected ratio of final graph's with to height,
#     #     used to select the constrained axis.
    
#     # Returns
#     # --------
#     # zoom: float, from 1 to 20
#     # center: dict, gps position with 'lon' and 'lat' keys

#     # >>> print(zoom_center((-109.031387, -103.385460),
#     # ...     (25.587101, 31.784620)))
#     # (5.75, {'lon': -106.208423, 'lat': 28.685861})
#     # """
#     # if lons is None and lats is None:
#     #     if isinstance(lonlats, tuple):
#     #         lons, lats = zip(*lonlats)
#     #     else:
#     #         raise ValueError(
#     #             'Must pass lons & lats or lonlats'
#     #         )
    
#     maxlon, minlon = max(lons), min(lons)
#     maxlat, minlat = max(lats), min(lats)
#     center = {
#         'lon': round((maxlon + minlon) / 2, 6),
#         'lat': round((maxlat + minlat) / 2, 6)
#     }
    
#     # longitudinal range by zoom level (20 to 1)
#     # in degrees, if centered at equator
#     lon_zoom_range = np.array([
#         0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
#         0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
#         47.5136, 98.304, 190.0544, 360.0
#     ])
    
#     margin = 6
#     width_to_height = 3
#     height = (maxlat - minlat) * margin * width_to_height
#     width = (maxlon - minlon) * margin
#     lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
#     lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
#     zoom = round(min(lon_zoom, lat_zoom), 2)

    
#     return zoom, center

def zoom_center(bbox, #lons: tuple = None, lats: tuple = None, lonlats: tuple = None,
                format: str = 'lonlat', projection: str = 'mercator',
                width_to_height: float = 2.0):
    """Finds optimal zoom and centering for a plotly mapbox.
    Must be passed (lons & lats) or lonlats.
    Temporary solution awaiting official implementation, see:
    https://github.com/plotly/plotly.js/issues/3434
    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    lonlats: tuple, optional, gps locations
    format: str, specifying the order of longitud and latitude dimensions,
        expected values: 'lonlat' or 'latlon', only used if passed lonlats
    projection: str, only accepting 'mercator' at the moment,
        raises `NotImplementedError` if other is passed
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.
    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys
    >>> print(zoom_center((-109.031387, -103.385460),
    ...     (25.587101, 31.784620)))
    (5.75, {'lon': -106.208423, 'lat': 28.685861})
    See https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
    """
    # if lons is None and lats is None:
    #     if isinstance(lonlats, tuple):
    #         lons, lats = zip(*lonlats)
    #     else:
    #         raise ValueError(
    #             'Must pass lons & lats or lonlats'
    #         )

    # maxlon, minlon = max(lons), min(lons)
    # maxlat, minlat = max(lats), min(lats)
    maxlon, minlon = bbox[2], bbox[0]
    maxlat, minlat = bbox[3], bbox[1]
    
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }

    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])

    if projection == 'mercator':
        margin = 4
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)
    else:
        raise NotImplementedError(
            'projection is not implemented'
        )

    return zoom, center


def plot_single_windfarm_mapbox(clustered_data, wfid):
    
    # clustered_data = pd.read_csv("data/wt_data_final.csv")
    # wfid = 10710
    # plot_single_windfarm_mapbox(data, wfid)
    if (wfid == -1):
        return html.Div('Single turbines cannot be plotted!')
    current_wf = clustered_data[clustered_data["WFid"] == wfid]
    wf_geopoints = turf.points(current_wf[["lon", "lat"]].values.tolist())


    
    # Create grid to put on wind farm and store in list
    bbox = turf.bbox(wf_geopoints)
    bbox_buff = [bbox[0] - 0.01, bbox[1]-0.01, bbox[2]+0.01, bbox[3]+0.01]

    # Retrieve central loaction of points and store in dictionary later to center maps in layout 
    # zoom, center = zoom_center(current_wf["lon"], current_wf["lat"])
    zoom, center = zoom_center(bbox_buff)

    # bbox_buff = bbox
    layer=turf.square_grid(bbox_buff,1000, {"units": 'meters'})

    # Retrieve all turbines in bounding box of +- 0.05°
    ll = np.array([(center["lat"]-1), (center["lon"]-1)])  # lower-left
    ur = np.array([(center["lat"]+1), (center["lon"]+1)])  # upper-right
    inidx = np.all(np.logical_and(ll <= clustered_data[["lat", "lon"]], clustered_data[["lat", "lon"]] <= ur), axis=1)
    data_in_box = clustered_data[inidx]
    # data_in_box[wfid_column] = data_in_box[wfid_column].apply(str)

    data_in_box.loc[data_in_box["WFid"] != wfid, "Color"] = "#FFC000"
    data_in_box.loc[data_in_box["WFid"] == wfid, "Color"] = "#FF0000"
    
    fig = go.Figure(go.Scattermapbox(
        lon=list(data_in_box["lon"]),
        lat=list(data_in_box["lat"]), 
        mode='markers', 
        name = "", 
        marker=dict(color=data_in_box["Color"]), 
        hovertemplate = [f'Windfarm ID: {string1}<br>Turbine Spacing (m): {string2}<br>Number of turbines: {string3}<br>Elevation (m): {string4}<br>Land Cover: {string5}<br>Landform: {string6}<br>Country: {string7}<br>Continent: {string8}<br>Shape: {string9}'
                    for string1, string2, string3, string4, string5, string6, string7, string8, string9 in zip(data_in_box["WFid"], data_in_box["Turbine Spacing"], data_in_box["Number of turbines"], data_in_box["Elevation"], data_in_box["Land Cover"], data_in_box["Landform"], data_in_box["Country"],data_in_box["Continent"],  data_in_box["Shape"])]
        ))
    fig.update_mapboxes(
                style= "mapbox://styles/zwiefele/cl4dap44m001d15pfttaws59k", 
                accesstoken="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw"
                # background-opacity = 0.8
                )

    fig.update_layout(
        mapbox=dict(layers=[dict(sourcetype ='geojson',source =layer,type = 'line', color = '#454545',opacity = 0.2,line=dict(width=1))]), 
        margin=dict(l=0, r=0, t = 0, b=0),
        hoverlabel=dict(
            bgcolor="#AEDCC8",
            font_size=11,
            font_family='Montserrat, sans-serif'
        )
        )
    fig.layout.mapbox.center = center
    fig.layout.mapbox.zoom = zoom
    # fig.show()



    return fig

# data = pd.read_csv("data/wt_data_final.csv")
# wfid = 140
# plot_single_windfarm_mapbox(data, wfid)

def plot_wf_histograms(filtered_wt_data, filtered_wf_data, x_axis = "Country"):

    filtered_wt_data['grouping'] = 'contained in wind farm'
    filtered_wt_data.loc[(filtered_wt_data["WFid"] == -1), 'grouping'] = 'single turbine'
    if x_axis in ["Country", "Continent", "Land Cover", "Landform", "Shape" ]:
        # Fig 1 
        x_axis_label = x_axis
        xaxis_groupby = filtered_wf_data[x_axis].value_counts()
        category_order_names = xaxis_groupby.keys().tolist()
        xaxis_groupby = xaxis_groupby.reset_index().sort_values(x_axis)

        fig1_histwf = px.histogram(xaxis_groupby,x=x_axis,y ="index", color_discrete_sequence=['#F46281'], 
                        category_orders={x_axis: category_order_names}, labels={"index": "Count of Wind farms", x_axis: x_axis})

        # Fig 2
        wfsizedistr_datatable =filtered_wf_data.groupby(x_axis)["Number of turbines"].describe().round(2).loc[category_order_names].reset_index()
        fig2_hist_wfsize = [dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in wfsizedistr_datatable.columns],
            data=wfsizedistr_datatable.to_dict('records'), 
            style_as_list_view=True,
            fixed_rows={'headers': True},
            style_cell={'textAlign': 'center', 
                'fontSize':9, 
                'font-family':'Verdana, sans-serif', 

                },
            style_table={"padding-left":"10px","padding-right":"10px", "background-color":"#F9F9F9", "color":"#2C3333"},
            style_header={
                'backgroundColor': '#2C3333',
                'color': 'white'
            },
            style_data={
                'height': 'auto',
                'minWidth': '8px', 
                # 'width': 'auto', 
                'maxWidth': '15px',     
                'whiteSpace': 'pre-line',
                "background-color":"#F4F4F4",
            },
            sort_action="native",

        
                )
            ]

        categories_fig3 = np.unique(filtered_wt_data[x_axis])
        not_contained = [i for i in categories_fig3 if i not in category_order_names]
        for x in not_contained:
            category_order_names.append(x)

        # category_order_names = category_order_names +  not_contained
        # categories_fig3[~(categories_fig3 in category_order_names)]
        fig3_histwt =  px.histogram(filtered_wt_data, y = x_axis, color="grouping",color_discrete_sequence=["#F46281", "#f4a261"], 
                        category_orders={ x_axis: category_order_names,"grouping":['in wind farm','single turbine']})



    else:
        # Fig 1
        if x_axis in ["Elevation", "Turbine Spacing"]:
            x_axis_label = x_axis + " (m)"
        else: x_axis_label = x_axis
        fig1_histwf = px.histogram(filtered_wf_data,y =x_axis,opacity=0.8, color_discrete_sequence=['#F46281'], nbins = 200,  
            text_auto='.2s', labels={
                        "index": "Count of Wind farms",
                        x_axis: x_axis_label,
                    }
                    )

        # Fig 2
        turbingesdist_datatable =filtered_wf_data[x_axis].describe().round(2).reset_index()
        fig2_hist_wfsize = [dash_table.DataTable(
            # id='table-container',
            columns=[{"name": i, "id": i} for i in turbingesdist_datatable.columns],
            data=turbingesdist_datatable.to_dict('records'), 
            style_as_list_view=True,
            fixed_rows={'headers': True},
            style_cell={'textAlign': 'center', 
                # "width":"20%", 
                'fontSize':9, 
                'font-family':'Verdana, sans-serif', 
                # 'padding-left':'10px',
                # 'padding-right':'10px',
                },
            style_table={"padding-left":"10px","padding-right":"10px", "background-color":"#F4F4F4", "color":"#2C3333"},
            style_header={
                'backgroundColor': '#2C3333',
                'color': 'white'
            },
            style_data={
                'height': 'auto',
                'minWidth': '8px', 
                # 'width': 'auto', 
                'maxWidth': '15px',     
                'whiteSpace': 'pre-line',
                "background-color":"#F4F4F4",
            },
            sort_action="native",    
                )
            ]

        
        fig3_histwt =  px.histogram(filtered_wt_data, y = x_axis,  opacity=0.8, color="grouping",color_discrete_sequence=["#F46281", "#f4a261"], 
                        category_orders={ "grouping":['turbines in wind farms','single turbines']}, nbins=200)



    fig1_histwf.update_layout(

        xaxis_title="Wind Farms count",
        yaxis_title=x_axis_label, 
        margin = {'r':0,'t':40,'l':0,'b':0}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='#F4F4F4', 
        font_family='Montserrat, sans-serif',
        font_color="#2C3333",
        title_font_family='Montserrat, sans-serif',
        title_font_color="#2C3333",
        legend_title_font_color="#2C3333",
        hovermode ="y unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Montserrat, sans-serif"
        ),
        )
    fig1_histwf.update_traces(hovertemplate='Number of wind farms: %{x}') #

    


    fig3_histwt.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Montserrat, sans-serif"
        ),
        # title="Wind Turbines",
        xaxis_title="Wind Turbines count",
        yaxis_title=x_axis_label,
        legend_title=None,
        margin = {'r':15,'t':30,'l':15,'b':15}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='#F4F4F4', 
        font_family='Montserrat, sans-serif',
        font_color="#2C3333",
        title_font_family='Montserrat, sans-serif',
        title_font_color="#2C3333",
        hovermode ="y unified"

    )
    fig3_histwt.update_traces(hovertemplate='%{x}') #



    return fig1_histwf, fig2_hist_wfsize, fig3_histwt

def plot_wf_poster(filtered_wt_data, filtered_wf_data, seed = 0, sorting_condition="Number of turbines",  plot_rows=5, plot_col = 5):
    # seed = 0
    # sorting_condition="Number of turbines"
    # plot_rows=3
    # plot_col = 3
    # filtered_wt_data = pd.read_csv("data/wt_data_final.csv")
    # filtered_wf_data = pd.read_csv("data/wf_data_final.csv")
    # filtered_wt_data = filtered_wt_data[filtered_wt_data["Land Cover"] == "Open forest"]
    # filtered_wf_data = filtered_wf_data[filtered_wf_data["Land Cover"] == "Open forest"]
    clustered_data = filtered_wt_data

    wfids = filtered_wf_data.WFid.to_list()
    random.seed(seed)
    random_wfsids = sample(wfids,plot_rows*plot_col)
    random_wfs_ids = filtered_wf_data[filtered_wf_data["WFid"].isin(random_wfsids)].sort_values(sorting_condition)["WFid"].to_list()

    # Initialize figure
    specs = [{"type": 'mapbox'}]
    i = 1
    while (i  < (plot_col)):
        specs.append( {"type": 'mapbox'})
        i = i+1
    j = 0
    specs_list = []
    while (j < (plot_rows)):
        specs_list.append(specs)
        j = j+1

    # create fig and set common attributes
    fig = make_subplots(rows=plot_rows, cols=plot_col, horizontal_spacing = 0.01,vertical_spacing = 0.02,
         specs= specs_list)
        # [{"type": 'mapbox'}, {"type": 'mapbox'}, {"type": 'mapbox'}]])
    fig.update_mapboxes(
                # layers = list(layers.values()), 
                style= "mapbox://styles/zwiefele/cl4dap44m001d15pfttaws59k", 
                accesstoken="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw",
                # zoom=10
                )
    fig.update_layout(
        title = "Random Wind Farms" ,
        showlegend=False, 
        )
    # colors = ["#FFFC00", "#FFFC00", "#FFFC00", "#FFFC00", "#FFFC00", "#FFFC00", "#FFFC00", "#FFFC00", "#FFFC00"]

    x = 0

    # Initialize lists where for centers and grids 
    zooms = []
    centers = []
    grids = []
    
    # x = 2
    # figs = []
    # For each selected wind farm 
    for i in range(1, plot_rows + 1):
        for j in range(1, plot_col + 1):
            # #update common attributes:

            # Get wind farm through id
            # current_wfid = 10710

            current_wfid = random_wfs_ids[x]
            current_wf = clustered_data[clustered_data["WFid"] == current_wfid]
            wf_geopoints = turf.points(current_wf[["lon", "lat"]].values.tolist())

            
            # Create grid to put on wind farm and store in list
            bbox = turf.bbox(wf_geopoints)
            bbox_buff = [bbox[0] - 0.01, bbox[1]-0.01, bbox[2]+0.01, bbox[3]+0.01]
            # bbox_buff =bbox
            layer=turf.square_grid(bbox_buff,1000, {"units": 'meters'} )
            grids.append(layer)

            # Retrieve central loaction of points and store in 
            # dictionary later to center maps in layout 
            # zoom, center = zoom_center(current_wf["lon"], current_wf["lat"])
            zoom, center = zoom_center(bbox_buff)
            # zoom = 13
            # cent_dic = {'lat':center["geometry"]["coordinates"][1],'lon':center["geometry"]["coordinates"][0]}.copy()
            centers.append(center)
            zooms.append(zoom)

            # Retrieve all turbines in bounding box of +- 0.05°
            ll = np.array([(center["lat"]-1), (center["lon"]-1)])  # lower-left
            ur = np.array([(center["lat"]+1), (center["lon"]+1)])  # upper-right
            inidx = np.all(np.logical_and(ll <= clustered_data[["lat", "lon"]], clustered_data[["lat", "lon"]] <= ur), axis=1)
            data_in_box = clustered_data[inidx]
            data_in_box["group"] = 0
            data_in_box.loc[data_in_box["WFid"].isin([current_wfid]),"group"] = "#FF0000"
            data_in_box.loc[~data_in_box["WFid"].isin([current_wfid]),"group"] = "#FFC000"
            fig.add_trace(go.Scattermapbox(
                lon=list(data_in_box["lon"]),
                lat=list(data_in_box["lat"]), 
                mode='markers', 
                name='',
                marker=dict(color=data_in_box["group"]), 
                text = ["test"],
                hovertemplate = [f'Windfarm ID: {string1}<br>Turbine Spacing (m): {string2}<br>Number of turbines: {string3}<br>Elevation (m): {string4}<br>Land Cover: {string5}<br>Landform: {string6}<br>Country: {string7}<br>Continent: {string8}<br>Shape: {string9}'
                    for string1, string2, string3, string4, string5, string6, string7, string8, string9 in zip(data_in_box["WFid"], data_in_box["Turbine Spacing"], data_in_box["Number of turbines"], data_in_box["Elevation"], data_in_box["Land Cover"], data_in_box["Landform"], data_in_box["Country"],data_in_box["Continent"],  data_in_box["Shape"])]
            ), row=i, col=j)

            x=x+1

    temp= min(plot_rows, plot_col)

    fig.update_layout(
        height = 300+temp*150, 
        width = 400+temp*150, 
        autosize = True, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='#F4F4F4', 
        margin = {'r':0,'t':0,'l':0,'b':0}, 
        hoverlabel=dict(
            bgcolor="#AEDCC8",
            font_size=11,
            font_family='Montserrat, sans-serif'
        )
    )
    # Update grid layers of figures 
    for m, g in zip(fig.data, grids):
        exec("fig.update_layout("+ str(m.subplot) + "=dict(layers=[dict(sourcetype = 'geojson',source ="+str(g)+",type = 'line', color = '#454545',opacity = 0.2,line=dict(width=1))]))")
        #
                
    # Update centers of figures 
    for m, c in zip(fig.data, centers):
        exec("fig.layout." + m.subplot+"[\"center\"] = " + str(c) )
    # Update centers of figures 
    for m, z in zip(fig.data, zooms):
        exec("fig.layout." + m.subplot+"[\"zoom\"] = " + str(z) )
    # fig.show()

    return fig


# Read data
data_windfarms = pd.read_csv("data/wf_data_final.csv")#.iloc[1:5000]

data_windturbines = pd.read_csv("data/wt_data_final.csv")
# data_windturbines[data_windturbines["WFid"] == -1]
# Create dropdown Menu contents
landcover_options = [{'label': i, 'value': i} for i in sorted(data_windfarms["Land Cover"].unique())]
country_options = [{'label': i, 'value': i} for i in sorted(data_windturbines["Country"].unique())]
continent_options = [{'label': i, 'value': i} for i in sorted(data_windturbines["Continent"].unique())]
landform_options = [{'label': i, 'value': i} for i in sorted(data_windturbines["Landform"].unique())]
shape_options = [{'label': i, 'value': i} for i in data_windfarms["Shape"].dropna().unique()]
column_names = ['Country', 'Continent', 'Land Cover','Landform','Shape', 'Number of turbines','Elevation' ,'Turbine Spacing'   ]
x_axis_options = [{'label': i, 'value': i} for i in column_names]
# Defaults
landcover_defaults = [o["value"] for o in landcover_options]
country_defaults = [o["value"] for o in country_options]
continent_defaults = [o["value"] for o in continent_options]
landform_defaults = [o["value"] for o in landform_options]
shape_defaults = [o["value"] for o in shape_options]
x_axis_options_default = [o["value"] for o in x_axis_options]


# # Map layers for leaflet
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"
mapbox_token ="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw"  # settings.MAPBOX_TOKEN
mapbox_ids = ["light-v9", "dark-v9", "streets-v9", "outdoors-v9", "satellite-streets-v9"]



# Styles for tabs 
tabs_styles = {
    'height': '35px', 
    'display':'flex', 
    'marginLeft':'5px',
    'marginRight':'5pxs',
    "width":"99%",
    "textAlign":"center"

}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '5px',
    'fontWeight': 'bold',
    'backgroundColor':'#fcfcfc',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#65BB95',
    'color': "#FFFFFF",
    'padding': '6px'
}



# data = geojson_wf,
# data = geojson_wt, 
# Create data overlays windfarms - windturbine for Map Tab 1
    # Visualizations
# point_to_layer = assign("function(feature, latlng, context) {return L.circleMarker(latlng);}")
# geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=point_to_layer))
cluster_wf = dl.GeoJSON( id="geojson",  format = "geobuf",cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100, "maxZoom":11})#,children=[dl.Popup("Displayed Windfarm")]
cluster_wt = dl.GeoJSON(id="geojson_wt",   format = "geobuf", cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100, "maxZoom":11})#,children=[dl.Popup("Displayed Windfarm")]
#format="geobuf",


# Create app
app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX], assets_folder='assets')
server = app.server
# application = app.server
app.config.suppress_callback_exceptions = True

# Define layout 
app.layout = html.Div([

    
    # Filter Options
    html.Div(children=[
        html.H2("Visualizing Wind Farms", className = "title"),
        dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(children=[], className="card-title", id = "filter_application"),
                        html.P("of 20.607 Wind Farms", className="card-text"),
                    ]
                ),
            ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(children=[], className="card-title", id = "filter_application_wts"),
                    html.P("of 359.947 Wind Turbines", className="card-text"),
                ]
            ),
        ),

        html.Button(
            "!",
            id="popover-alt-target",
            className="popover-alt-target-1",
        ),
        dbc.Popover(

            id = "popover_content",
            body=True,
            target="popover-alt-target",
            trigger="hover",
            class_name="popover"
        ),
        html.Button(id='submit-button-state', n_clicks=0, children='Apply Filter', className="filterButton"),
        daq.ToggleSwitch(
            id='my-toggle-switch',
            value=False,  
            label='Show Filter',
            className = "toggleSwitch",
            size = 40, 
            color = "#68c49b",
            # theme = dbc.themes.MINTY
        ), 



        
        
        ], className = "headerClass"
        
    ), 
    

    html.Div(children  =[
        html.Div(children = [
                dbc.Container(
                        children=[
                            html.H6('Country'),
                            html.Details([
                            html.Summary('Select country...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_countries", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_country",
                                    options=country_options,
                                    value=country_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )               
                                
                                ])
                            ])
                    ], className="filterBoxes"),

                dbc.Container(
                        children=[
                            html.H6('Continent'),
                            html.Details([
                            html.Summary('Select continent...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_continent", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_continent",
                                    options=continent_options,
                                    value=continent_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )               
                                
                                ])
                            ])
                    ], className="filterBoxes"),

                dbc.Container(
                        children=[
                            html.H6('Land Cover'),
                            html.Details([
                            html.Summary('Select land cover...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_landcover", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_landcover",
                                    options=landcover_options,
                                    value=landcover_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )               
                                
                                ])
                            ])
                    ], className="filterBoxes"),

                    dbc.Container(
                        children=[
                            html.H6('Land Form'),
                            html.Details([
                            html.Summary('Select land form...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_landform", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_landform",
                                    options=landform_options,
                                    value=landform_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )               
                                
                                ]
                                )
                            ])
                    ], className="filterBoxes"),

                    dbc.Container(
                                    children=[
                                        html.H6('Shape'),
                                        html.Details([
                                        html.Summary('Select shape', className="app-summaries"),
                                        html.Br(),
                                        dbc.Col([
                                            dcc.Checklist(["All"],["All"], id="dd_all_shape", inline=True, className = "checkboxes_label_all"),
                                            dcc.Checklist(
                                                id="dd_shape",
                                                options=shape_options,
                                                value=shape_defaults,
                                                labelStyle = { 'marginLeft':'7px','display':'block'},
                                                className = "checkboxes_label"
                                                )               
                                            
                                            ]
                                            )
                                        ])
                                ], className="filterBoxes"), 
                ], className = "allFilterBoxesToprow"), 

            
            html.Div(children=[



                html.Div(children=[
                    html.H6('Number of Turbines'),
                    dcc.RangeSlider(1, 3296, 1, value=[1, 4086],marks=None, id='sd_turbines', tooltip={"placement": "bottom", "always_visible": True})
                ],  className = "sliderBox"),


                html.Div(children=[
                    html.H6('Elevation Level (m)'),
                    dcc.RangeSlider(-46, 4684, 1, value=[-46, 4684],marks=None, id='sd_elevation', tooltip={"placement": "bottom", "always_visible": True})
                ],  className ="sliderBox"),

                html.Div(children=[
                    html.H6('Turbine Spacing (m)'),
                    dcc.RangeSlider(10, 13155, 10, value=[10, 13155],marks=None, id='sd_distance', tooltip={"placement": "bottom", "always_visible": True})
                ], className="sliderBox"),

            ], className="sliders_class"), 
        ],  className = "allFilters", id = "allfilters"),



     


                
    dcc.Tabs([
        dcc.Tab(label='Map', children=[
            html.Div(children = [
                
            dbc.Spinner(children=[
                dbc.Container(children = [
                    dbc.Label("World Map", style = {'marginLeft':'5px'}),
                    html.Div(dl.Map([#dl.TileLayer(),        
                                dl.LayersControl(collapsed=False,
                                    children=[dl.BaseLayer(dl.LayerGroup(cluster_wf), name="Wind Farms", checked=True), 
                                    dl.BaseLayer(dl.LayerGroup(cluster_wt), name="Wind Turbines", checked=False)], id = "MapLeafletLayersControl"), 
                                dl.LayersControl(
                                    [dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="light-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Light", checked=True),
                                    dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="satellite-streets-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Satellite", checked=False), 
                                    dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="dark-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Dark", checked=False), 
                                    dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="outdoors-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Outdoor", checked=False)
                                                ]), 
                                dl.GestureHandling(), 
                                dl.MeasureControl(position="topleft", primaryLengthUnit="meters", primaryAreaUnit="hectares",
                                                        activeColor="#214097", completedColor="#972158"),
                                dl.ScaleControl(position="bottomleft")
                                

                            ], 
                    center=(33.256890, -3.810381), 
                    zoom=2, 
                    preferCanvas=True,
                    ),className = "MapBoxLeaflet")], style = {'display':'inline-grid'}), 
                ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),

            dbc.Container(children = [
                dbc.Label("Single Wind Farm", style ={'marginLeft':'-3%'}),
                html.Div(children = ["   Click on a marker to plot the related wind farm."], id = "singleWF",  className = "MapBox")], style = {"display":"inline-grid"})], className = "tab1")

        ], style=tab_style, selected_style=tab_selected_style),



        dcc.Tab(label='Frequency Distribution', children=[
            
            html.Div(children=[
                html.H6('y-Axis'),
                dcc.Dropdown(id="dd_xaxis", value=x_axis_options_default[1], options=x_axis_options, className = "checkboxes_label_all")
            ], style = {"display": "block", "width":"25%", "marginLeft":"15px"}), 
            
            dbc.Spinner(children=[

                html.Div(children = 
                    [
                    
                    dbc.Container(children = [
                        dbc.Label("Wind Turbines"),
                        html.Div(children=[dcc.Graph(id = "hist_wtcount_graph")])
                        ], className = "histComponent"),
                    dbc.Container(children = [
                        dbc.Label("Wind Farms"),
                        html.Div(children=[dcc.Graph(id = "hist_wfcount_graph")])
                        ], className = "histComponent"),
                    
                    dbc.Container(children = [
                        dbc.Label("Wind Farm Descriptive Summary Statistics"),
                        html.Div(id  = "hist_turbinescountgrouped_graph", children=[], style = {'height':'80vh'})
                        ], className = "histComponent"),

                    
    
                    ],
                style={'height': "100%", 'width': "100%", 'display':'flex' }

                )
            ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),
        ], style=tab_style, selected_style=tab_selected_style),



        dcc.Tab(label='Show me some Wind Farms!', children=[
            html.Div(children = [

                html.Div(children=[
                    html.H6('Sorting Feature'),
                    dcc.Dropdown(id="dd_sort", value="Continent", options=x_axis_options)
                    ], className = "posterFilterElement"),


                html.Div(children=[             
                    html.H6('Seed'),
                    dcc.Input(id='ip_seed', type='number', min=0, max=1000000, step=1, value = 0, placeholder="Seed")       
                    ], className = "posterFilterElement2" ),
                
                
                html.Div(children=[             
                    html.H6('Plot Rows'),
                    dcc.Input(id='ip_plotrows', type='number', min=1, max=10, step=1, value = 3, placeholder="Plot Rows")       
                    ], className = "posterFilterElement2"), 

                html.Div(children=[             
                    html.H6('Plot Columns'),
                    dcc.Input(id='ip_plotcols', type='number', min=1, max=10, step=1, value = 3 , placeholder="Plot Columns")       
                    ],  className = "posterFilterElement2"), 

                
                

            ], className= "posterFilter"), 
            # html.Div(
            dbc.Container(children = [
                dbc.Label("Random Wind Farms"),
                dbc.Spinner(children=[
                    html.Div(children=[dcc.Graph(id = "poster_graph", style={'height': '90%'})])
                ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),
            ], className = "posterGraph")
            # ]), className = "posterGraph")
        ], style=tab_style, selected_style=tab_selected_style),
        
    ], style = tabs_styles, id = "tabs"), 
    
        dcc.Tabs([
            dcc.Tab(label='EXQ1', children=[
                html.Div(children =["Which land form is predominant for the installation of windfarms in Austria?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='EXQ2', children=[
                html.Div(children =["Where do you find the biggest wind farms in the world? How is their turbine spacing distributed?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='Q1', children=[
                html.Div(children =["Which land cover is predominant for the installation of Wind Farms on a global scale?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),


            dcc.Tab(label='Q2', children=[
                html.Div(children =["How do wind farms in the USA, Germany and China compare in terms of size and frequency?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='Q3', children=[
                html.Div(children =["Where are the highest wind farms in the world located?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='Q4', children=[
                html.Div(children =["How does the turbine spacing of wind farms in Oceans and seas compare to wind farms on Agricultural land cover?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='Q5', children=[
                html.Div(children =["Filter the data for wind farms with more than 10 turbines and look at 3x3 random wind farms. Set the seed to 0. Which of the wind farms has the smallest spacing between the turbines?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='Q6', children=[
                html.Div(children =["Which of the wind farms (if any) are positioned on a summit or ridge?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),


            dcc.Tab(label='Q7', children=[
                html.Div(children =["Is there a question you would like to answer with the tool?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),
            
            dcc.Tab(label='FQ1', children=[
                html.Div(children =["Have you learned any new insights about the wind industry? If so, which ones?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='FQ2', children=[
                html.Div(children =["Did the visualization confirm any assumptions you had about the wind industry before?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),

            dcc.Tab(label='FQ3', children=[
                html.Div(children =["Can you give general feedback on the visualization in terms of user interface, functionalities, etc.?"], className = "questions")
                ], style=tab_style, selected_style=tab_selected_style),
            
        ], className=  "tabqt"),
    
   
    # html.Div(children = [data_windfarms.to_dict('list')], id = "store_all_wf_data", style = {'display':'none'}),
    # html.Div(children = [data_windturbines.to_dict('list')], id = "store_all_wt_data", style = {'display':'none'}),
    # dash_table.DataTable(data = data_windfarms.to_dict('records'), id = "store_all_wf_data"), 
    # dash_table.DataTable(data = data_windturbines.to_dict('records'),  id = "store_all_wt_data"), 

    dcc.Store(data = data_windfarms.to_dict('list'), id='store_all_wf_data', storage_type="memory"), 
    dcc.Store(data =  data_windturbines.to_dict('list'),id='store_all_wt_data', storage_type = "memory"),
    dcc.Store(id='filtered_wt_intermediate', storage_type="memory"), 
    dcc.Store(id='filtered_wf_intermediate', storage_type="memory"),
    # dbc.Spinner(children=[
    #      dcc.Store(data=[""], id = 'loader_stoer')
    # ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),
   
    # dbc.Row(dbc.Col(
    #     dbc.Spinner(children=[
],className = "allPage")



app.clientside_callback(
    """
    function(value) {
        if(value === true) {
            return {'display': 'block'};
        } else {
            return {'display': 'none'}
        }
    }
    """,
    Output('allfilters', 'style'),
    [Input('my-toggle-switch', 'value')]
)


app.clientside_callback(
   ClientsideFunction(
        namespace='clientside',
        function_name='filter_function'
    ),
    # Output(component_id="geojson", component_property='data'),
    # Output(component_id="geojson_wt", component_property='data'), 
    Output(component_id="filtered_wt_intermediate", component_property="data"),
    Output(component_id="filtered_wf_intermediate", component_property="data"),
    Output( "filter_application", "children"), 
    Output( "filter_application_wts", "children"), 

    Input('submit-button-state', 'n_clicks'),
    State('store_all_wt_data', 'data'), 
    State('store_all_wf_data', 'data'), 
    State(component_id="dd_landcover", component_property="value"),
    State(component_id="dd_country", component_property="value"),
    State(component_id="dd_continent", component_property="value"),
    State(component_id="sd_turbines", component_property="value"),
    State(component_id="dd_landform", component_property="value"), 
    State(component_id="sd_distance", component_property="value"), 
    State(component_id="sd_elevation", component_property="value"), 
    State(component_id="dd_shape", component_property="value")
)

# Checklist synchronisation Country


@app.callback(
    Output("dd_country", "value"),
    Output("dd_all_countries", "value"),
    Input("dd_country", "value"),
    Input("dd_all_countries", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_country":
        all_selected = ["All"] if set(selected_filter_var) == set(country_defaults) else []
    else:
        selected_filter_var = country_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation Land Cover
@app.callback(
    Output("dd_landcover", "value"),
    Output("dd_all_landcover", "value"),
    Input("dd_landcover", "value"),
    Input("dd_all_landcover", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_landcover":
        all_selected = ["All"] if set(selected_filter_var) == set(landcover_defaults) else []
    else:
        selected_filter_var = landcover_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation Land Form
@app.callback(
    Output("dd_landform", "value"),
    Output("dd_all_landform", "value"),
    Input("dd_landform", "value"),
    Input("dd_all_landform", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_landform":
        all_selected = ["All"] if set(selected_filter_var) == set(landform_defaults) else []
    else:
        selected_filter_var = landform_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation Shape
@app.callback(
    Output("dd_shape", "value"),
    Output("dd_all_shape", "value"),
    Input("dd_shape", "value"),
    Input("dd_all_shape", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_shape":
        all_selected = ["All"] if set(selected_filter_var) == set(shape_defaults) else []
    else:
        selected_filter_var = shape_defaults if all_selected else []
    return selected_filter_var, all_selected


# Checklist synchronisation continent
@app.callback(
    Output("dd_continent", "value"),
    Output("dd_all_continent", "value"),
    Input("dd_continent", "value"),
    Input("dd_all_continent", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_continent":
        all_selected = ["All"] if set(selected_filter_var) == set(continent_defaults) else []
    else:
        selected_filter_var = continent_defaults if all_selected else []
    return selected_filter_var, all_selected


# Callback to show single WF plot from Tab 1 on click 
@app.callback(
    Output("singleWF", "children"),

    Input("geojson", "click_feature"),
    Input("geojson_wt", "click_feature"),
    prevent_initial_call=True
)
def update_tooltip(feature1, feature2):
    triggered_id = ctx.triggered_id
    if (triggered_id == 'geojson'):
         return draw_wf_graph(feature1)
    elif triggered_id == 'geojson_wt':
         return draw_wf_graph(feature2)
    else: 
        dash.exceptions.PreventUpdate

def draw_wf_graph(feature):
    if feature is not None: 
        if "WFid" in feature["properties"]:
            wfid = int(str(feature['properties']["WFid"]))
            if (wfid == -1):
                return "Turbines that do not belong to a wind farm cannot be plotted!"
            fig = plot_single_windfarm_mapbox(data_windturbines, wfid)
            return dcc.Graph(figure=fig)
        else: 
            return "   Click on a marker to plot the related windfarm."
    else: 
        return "   Click on a marker to plot the related windfarm."



# TAB 2
@app.callback(
    Output(component_id="geojson", component_property='data'),
    Output(component_id="geojson_wt", component_property='data'), 
    # Output(component_id="loader_stoer", component_property='data'), 
    Input(component_id="filtered_wt_intermediate", component_property="data"),
    Input(component_id="filtered_wf_intermediate", component_property="data"),    

)


def update_tab1(filtered_wt_data_json, filtered_wf_data_json):
    filtered_wt_data_idx = pd.read_json(filtered_wt_data_json).iloc[:, 0].tolist()
    filtered_wf_data_idx = pd.read_json(filtered_wf_data_json).iloc[:, 0].tolist()
    filtered_wt_data = data_windturbines[data_windturbines.id.isin(filtered_wt_data_idx)][["lon", "lat", "popup", "WFid"]]
    filtered_wf_data = data_windfarms[data_windfarms.WFid.isin(filtered_wf_data_idx)][["lon", "lat", "popup", "WFid"]]
    # Tab 1
    geojson = dlx.dicts_to_geojson(filtered_wf_data.to_dict('records'), lon="lon")
    geojson_wt = dlx.dicts_to_geojson(filtered_wt_data.to_dict('records'), lon="lon")
    dicts = dlx.geojson_to_geobuf(geojson)
    dicts_wt = dlx.geojson_to_geobuf(geojson_wt)

    return dicts, dicts_wt#, [""]
    
# TAB 2
@app.callback(

    Output(component_id="hist_wfcount_graph", component_property='figure'),
    Output(component_id="hist_turbinescountgrouped_graph", component_property='children'), 
    Output(component_id="hist_wtcount_graph", component_property='figure'), 
    # Output(component_id="poster_graph", component_property='figure'),

                
    Input(component_id="dd_xaxis", component_property="value"), 
    Input(component_id="filtered_wt_intermediate", component_property="data"),
    Input(component_id="filtered_wf_intermediate", component_property="data"),    

)
def update_tab2( value_xaxis,  filtered_wt_data_json, filtered_wf_data_json,):
    #Read data
    filtered_wt_data_idx = pd.read_json(filtered_wt_data_json).iloc[:, 0].tolist()
    filtered_wf_data_idx = pd.read_json(filtered_wf_data_json).iloc[:, 0].tolist()
    filtered_wt_data = data_windturbines[data_windturbines.id.isin(filtered_wt_data_idx)]
    filtered_wf_data = data_windfarms[data_windfarms.WFid.isin(filtered_wf_data_idx)]

    histogram_plots  = plot_wf_histograms(filtered_wt_data, filtered_wf_data, x_axis = value_xaxis )

    return histogram_plots[0], histogram_plots[1], histogram_plots[2]#, poster_figure


# TAB 3 
@app.callback(
    Output(component_id="poster_graph", component_property='figure'),
    
    Input(component_id="ip_seed", component_property="value"),
    Input(component_id="ip_plotrows", component_property="value"),
    Input(component_id="ip_plotcols", component_property="value"),
    Input(component_id="dd_sort", component_property="value"),
    # Input(component_id="filtered_wt_intermediate", component_property="data"),
    Input(component_id="filtered_wf_intermediate", component_property="data"),    

)
def update_tab3(value_seed, value_pr, value_pc,value_sort,  filtered_wf_data_json):
    # filtered_wt_data_idx = pd.read_json(filtered_wt_data_json).iloc[:, 0].tolist()
    filtered_wf_data_idx = pd.read_json(filtered_wf_data_json).iloc[:, 0].tolist()
    # filtered_wt_data = data_windturbines[data_windturbines.id.isin(filtered_wt_data_idx)]
    filtered_wf_data = data_windfarms[data_windfarms.WFid.isin(filtered_wf_data_idx)]

    poster_figure =  plot_wf_poster(data_windturbines, filtered_wf_data,  seed = value_seed, plot_col= value_pc, plot_rows =value_pr, sorting_condition= value_sort)
    # poster_figure.show()
    return  poster_figure

# Error Calllback 
@app.callback(
    Output("popover_content", "children"),
    Output("popover-alt-target", "style"),
    Input(component_id="filter_application_wts", component_property="children"),
    Input(component_id="filter_application", component_property="children"),
    Input(component_id="ip_plotrows", component_property="value"),
    Input(component_id="ip_plotcols", component_property="value"),
    Input(component_id="tabs", component_property="value"),

)
def update_error(input_string_wt, input_string_wf, pr, pc, tabvalues):

    if (str(input_string_wt) == "0"):
        return "There are no turbines to the applied filters!", {'backgroundColor':'#E55934', 'border':'1px solid #E55934', "color":"#fff"}
    elif((int(str(input_string_wf).replace(".", "")) < pr*pc) and (tabvalues   == "tab-3")):
        return "Less wind farms than traces for Poster plot!", {'backgroundColor':'#E55934', 'border':'1px solid #E55934', "color":"#fff"}
    else:
        return "", {'display':'none'} 




# if __name__ == '__main__':
#     app.run_server(debug = False)
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

    # application.run(port=8080, debug = True)