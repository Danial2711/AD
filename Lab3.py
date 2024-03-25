from spyre import server
import pandas as pd
from matplotlib.ticker import MaxNLocator

class SetData(server.App):
    title = "NOAA Data Visualization"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA Data',
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": 'coefficient',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Region',
            "options": [{"label": "Vinnytsya", "value": "1"},
                        {"label": "Volyn", "value": "2"},
                        {"label": "Dnipropetrovs'k", "value": "3"},
                        {"label": "Donets'k", "value": "4"},
                        {"label": "Zhytomyr", "value": "5"},
                        {"label": "Transcarpathia", "value": "6"},
                        {"label": "Zaporizhzhya", "value": "7"},
                        {"label": "Ivano-Frankivs'k", "value": "8"},
                        {"label": "Kiev", "value": "9"},
                        {"label": "Kirovohrad", "value": "10"},
                        {"label": "Luhans'k", "value": "11"},
                        {"label": "L'viv", "value": "12"},
                        {"label": "Mykolayiv", "value": "13"},
                        {"label": "Odessa", "value": "14"},
                        {"label": "Poltava", "value": "15"},
                        {"label": "Rivne", "value": "16"},
                        {"label": "Sumy", "value": "17"},
                        {"label": "Ternopil'", "value": "18"},
                        {"label": "Kharkiv", "value": "19"},
                        {"label": "Kherson", "value": "20"},
                        {"label": "Khmel'nyts'kyy", "value": "21"},
                        {"label": "Cherkasy", "value": "22"},
                        {"label": "Chernivtsi", "value": "23"},
                        {"label": "Chernihiv", "value": "24"},
                        {"label": "Crimea", "value": "25"}],
            "key": 'region',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Year',
            "key": 'year',
            "value": '',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Week Range (e.g., 1-10)',
            "key": 'week_range',
            "value": '',
            "action_id": "update_data"
        }
    ]

    controls = [{
        "type": "hidden",
        "id": "update_data"
    }]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        }
    ]

    def getData(self, params):
        data = pd.read_csv("full.csv")
        return data
    
    def filterData(self, data, params):
        region = int(params['region'])
        year = int(params['year'])
        week_range = [int(x) for x in str(params['week_range']).split('-')]
        filtered_data = data[(data['Area'] == region) & (data['Year'] == year) & (data['Week'] >= week_range[0]) & (data['Week'] <= week_range[1])]
        return filtered_data

    def getTable(self, params):
        df = self.getData(params)
        filtered_df = self.filterData(df, params)
        columns = ['Year', 'Week', params['coefficient'], 'Area']
        return filtered_df.loc[:, columns]

    def getPlot(self, params):
        df = self.getData(params)
        filtered_df = self.filterData(df, params)
        ticker = params['coefficient']
        region_index = int(params['region'])
        region_name = [option['label'] for option in self.inputs[1]['options'] if option['value'] == str(region_index)]
        region_name = region_name[0] if region_name else "Unknown Region"
        plt_obj = filtered_df.plot(x='Week', y=ticker)
        plt_obj.set_ylabel("Value")
        plt_obj.set_xlabel("Week")
        plt_obj.set_title(f"Plot for region {region_name} in {int(params['year'])}")
        plt_obj.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt_obj.grid(True)
        plot = plt_obj.get_figure()
        return plot

if __name__ == '__main__':
    app = SetData()
    app.launch()