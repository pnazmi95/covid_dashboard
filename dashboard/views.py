from django.shortcuts import render
import pandas as pd

df3 = pd.read_json(
    'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')


def index(request):
    confirmed_global = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    total_infected = confirmed_global[confirmed_global.columns[-1]].sum()
    hr_bar_data = confirmed_global[
        ['Country/Region', confirmed_global.columns[-1]]
    ].groupby(by='Country/Region').sum()
    hr_bar_data = hr_bar_data.reset_index()
    hr_bar_data.columns = ['Country/Region', 'Values']
    hr_bar_data = hr_bar_data.sort_values(by='Values', ascending=False)
    country_names = hr_bar_data['Country/Region'].values.tolist()
    country_values = hr_bar_data['Values'].values.tolist()
    data_for_world_map = map_data_calc(country_names, hr_bar_data)
    context = {
        'total_infected': total_infected,
        'country_names': country_names,
        'country_values': country_values,
        'data_for_world_map': data_for_world_map,
    }
    return render(request, 'dashboard/index.html', context)


def map_data_calc(country_names, hr_bar_data):
    data_for_heat_map = []
    for country in country_names:
        try:
            tempdf = df3[df3['name'] == country]
            temp = {}
            temp["code3"] = list(tempdf["code3"].values)[0]
            temp["name"] = country
            temp["value"] = hr_bar_data[
                hr_bar_data['Country/Region'] == country
                ]['Values'].sum()
            temp["code"] = list(tempdf["code"].values)[0]
            data_for_heat_map.append(temp)
        except:
            pass

        data_for_heat_map.append(
            {
                "code3": "USA",
                "name": "US",
                "value": hr_bar_data[
                    hr_bar_data['Country/Region'] == "US"
                    ]['Values'].sum(),
                "code": "US"
            }
        )

        data_for_heat_map.append(
            {
                "code3": "IRN",
                "name": "Iran",
                "value": hr_bar_data[
                    hr_bar_data['Country/Region'] == "Iran"
                    ]['Values'].sum(),
                "code": "IR"
            }
        )

    return data_for_heat_map
