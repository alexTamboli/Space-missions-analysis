import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go


from iso3166 import countries
<<<<<<< HEAD
# from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.seasonal import seasonal_decompose
=======
# from statsmodels.tsa.arima_model import ARIMA
# from statsmodels.tsa.seasonal import seasonal_decompose
>>>>>>> b746350cf57b202f47dec56e9be38681d2e0bbfb

import matplotlib
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from collections import OrderedDict


df = pd.read_csv('dataset/Space_Corrected.csv')
df.columns = [
    'Unnamed: 0', 
    'Unnamed: 0.1', 
    'Company Name', 
    'Location', 
    'Datum', 
    'Detail', 
    'Status Rocket', 
    'Rocket', 
    'Status Mission'
]
df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)

df['Rocket'] = df['Rocket'].fillna(0.0).str.replace(',', '')
df['Rocket'] = df['Rocket'].astype(np.float64).fillna(0.0)
df['Rocket'] = df['Rocket'] * 1000000
df['date'] = pd.to_datetime(df['Datum'], infer_datetime_format=True)
df['year'] = df['date'].apply(lambda datetime: datetime.year)
df['month'] = df['date'].apply(lambda datetime: datetime.month)
df['weekday'] = df['date'].apply(lambda datetime: datetime.weekday())

countries_dict = {
            'Russia' : 'Russian Federation',
            'New Mexico' : 'USA',
            "Yellow Sea": 'China',
            "Shahrud Missile Test Site": "Iran",
            "Pacific Missile Range Facility": 'USA',
            "Barents Sea": 'Russian Federation',
            "Gran Canaria": 'USA'
        }
df['country'] = df['Location'].str.split(', ').str[-1].replace(countries_dict)

country_dict = dict()
for c in countries:
    country_dict[c.name] = c.alpha3
df['alpha3'] = df['country']
df = df.replace(
    {
        "alpha3": country_dict
    }
)
df.loc[df['country'] == "North Korea", 'alpha3'] = "PRK"
df.loc[df['country'] == "South Korea", 'alpha3'] = "KOR"


# Top navbar
st.set_page_config(page_title="Space Missions Analysis", page_icon=":guardsman:", layout="wide")
    
with st.sidebar:
    st.title('Space Missions Analysis')
    pages = ['Home', 
             'About Data', 
             'Dataset Overview', 
             'Geo Analysis', 
             'Interesting Factors', 
             'The Cold war',
             'Best Every Year',
             'Time Series Decomposition',
             'India`s Place'
             ]
    page = st.radio('Navigation', pages)
    if page == 'About Data':
        st.write('## Select a dataset')
        datasets = ['Dataset 1', 'Dataset 2', 'Dataset 3']
        selected_dataset = st.radio('', datasets)
        


# Create main panel
main_panel = st.container()
with main_panel:
    st.title(page)
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    if page == 'Home':
        st.subheader('Data Analytics and Visualization Project')
        st.markdown(''' 
        ### Members
        1. Alex Tamboli - 2020110
        2. Ashish Gupta - 2020110
        3. Chinmay Badoliya - 2020110
        4. Nishesh Jain - 202011050
        5. Prashant Kumar - 2020110
        ''')
        
    
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'About Data':
        st.markdown(''' The Space Missions Analysis dataset contains information on space missions launched by various countries around the world from 1957 to present. The data includes details such as the launch date, country of origin, rocket used, mission status, and more. The dataset provides valuable insights into the history and trends of space exploration, and can be used to analyze the involvement of different countries in space missions, the success rates of missions, and the evolution of rocket technology over time. Through data visualization, this dataset can help to provide a deeper understanding of the past, present, and future of space exploration. ''')
        st.write('## Data Frame')
        st.dataframe(df)
        missed = pd.DataFrame()
        missed['column'] = df.columns
        percent = list()
        for col in df.columns:
            percent.append(round(100* df[col].isnull().sum() / len(df), 2))
        missed['percent'] = percent
        missed = missed.sort_values('percent')
        missed = missed[missed['percent']>0]
        fig = px.bar(
            missed, 
            x='percent', 
            y="column", 
            orientation='h', 
            title='Missed values percent for every column (percent > 0)', 
            width=600,
            height=200 
        )
        st.plotly_chart(fig)

        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Dataset Overview':
        st.write(' The higher number of rocket launches by certain countries can be attributed to a combination of historical context, technological advancements, and military applications.')
        ds = df['Company Name'].value_counts().reset_index()
        ds.columns = ['Company', 'Number of Launches']
        ds = ds.sort_values(['Number of Launches'], ascending=False)
        fig = px.bar(ds, 
                    x='Number of Launches', 
                    y="Company", 
                    orientation='h', 
                    title='Number of Launches by Every Company',
                    labels={'Number of Launches': 'Number of Launches', 'Company': 'Company Name'},
                    height=800,
                    width=900,
                    template='simple_white'
                    )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1
            ),
            yaxis=dict(
                title='',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1,
                tickfont=dict(size=12),
                automargin=True
            ),
            font=dict(
                family='Arial',
                size=14,
                color='black'
            )
        )
        fig.update_traces(
            texttemplate='%{x}',
            textposition='outside'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        
        #----------------------------------------------------------------------------------------------------
        ds = df['Company Name'].value_counts().reset_index()
        ds.columns = ['Company', 'Number of Launches']
        trace = go.Bar(
            x=ds['Number of Launches'],
            y=ds['Company'],
            orientation='h',
            text=ds['Number of Launches'],
            textposition='outside',
            marker=dict(color='#1f77b4')
        )
        layout = go.Layout(
            title='Number of Launches by Every Company',
            xaxis=dict(
                title='Number of Launches',
                tickfont=dict(size=12),
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1
            ),
            yaxis=dict(
                title='Company Name',
                tickfont=dict(size=12),
                automargin=True
            ),
            font=dict(
                family='Arial',
                size=14,
                color='black'
            ),
            height=800,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('''
        ### Insights

        1.**Historical Context**: The USSR and the USA were in a space race during the Cold War, which fueled significant investment in space exploration and a high number of rocket launches. Since then, these two countries have continued to maintain a strong presence in space exploration.

        2.**Technological Advancements**: NASA, Boeing, and SpaceX are all major players in the commercial space industry and have developed advanced rocket technology. This has allowed them to launch a larger number of rockets and achieve higher success rates than other countries.

        3.**Military Applications**: The US Air Force has been involved in launching rockets for military applications, such as spy satellites and communication networks, which require a high number of launches.

        ''')

        #--------------------------------------------------------------------------------------------------
        ds = df['Status Rocket'].value_counts().reset_index()
        ds.columns = ['status', 'count']
        ds = ds.sort_values('count', ascending=False)

        colors = ['rgb(75, 109, 153)', 'rgb(232, 114, 114)']

        fig = go.Figure(
            go.Pie(
                labels=ds['status'], 
                values=ds['count'],
                hole=0.5,
                marker=dict(colors=colors), 
                textfont=dict(size=14, color='black'),
                hoverinfo='label+percent',
                textinfo='label+percent'
            )
        )
        fig.update_layout(
            title=dict(
                text='Rocket Status',
                font=dict(size=24)
            ),
            margin=dict(l=0, r=0, t=80, b=0),
            font=dict(
                family='Arial',
                size=16,
                color='black'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(''' 
        ### Insights
        The fact that around 80% of rockets are not currently in use highlights the fact that historically rockets were designed as expendable vehicles, meaning they were only intended to be used once and then discarded. This resulted in a significant amount of waste and high launch costs, as a new rocket had to be built for each launch.
        ''')
        
        #---------------------------------------------------------------------------------------------
        ds = df['Status Mission'].value_counts().reset_index()
        ds.columns = ['mission_status', 'count']
        ds = ds.sort_values('count', ascending=False)

        colors = ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845']
        fig = px.bar(ds, 
                    x='mission_status', 
                    y='count', 
                    title='Mission Status Distribution',
                    color='mission_status',
                    color_discrete_sequence=colors,
                    height=600, 
                    width=800
                    )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            xaxis=dict(
                title='',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1,
                tickfont=dict(size=12),
                automargin=True
            ),
            font=dict(
                family='Arial',
                size=14,
                color='black'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        

        #------------------------------------------------------------------------------------
        colorscale = [[0, '#FFFFFF'], [0.5, '#72A1E5'], [1, '#153E75']]
        fig = go.Figure(go.Histogram(
            x=df['Rocket'],
            nbinsx=50,
            marker=dict(color='#72A1E5'),
            opacity=0.7,
            hovertemplate='Count: %{y}',
            name='Rocket Value'
        ))
        fig.update_layout(
            title=dict(
                text='Rocket Value Distribution',
                font=dict(size=24)
            ),
            xaxis=dict(
                title='Rocket Value (USD)',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1
            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1,
                tickfont=dict(size=12),
                automargin=True
            ),
            font=dict(
                family='Arial',
                size=16,
                color='black'
            )
        )
        fig.data[0].update(
            {'marker': {'colorscale': colorscale, 'showscale': True}}
        )
        st.plotly_chart(fig, use_container_width=True)

        
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Geo Analysis':
        st.write('The sunburst chart visualizes the number of rockets launched by different companies in various countries, along with the mission status of each launch. The chart is divided into three concentric circles, with the innermost circle representing countries, the middle circle representing companies within each country, and the outer circle representing the mission status of each launch.')
        sun = df.groupby(['country', 'Company Name', 'Status Mission'])['Datum'].count().reset_index()

        sun.columns = [
            'country', 
            'company', 
            'status', 
            'count'
        ]

        fig = px.sunburst(
            sun, 
            path=[
                'country', 
                'company', 
                'status'
            ], 
            values='count', 
            title='Sunburst chart for all countries',
            width=800,
            height=800 
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(''' 
        ### Insights
         If a particular country has a large segment in the chart, it means that the country has launched a significant number of rockets. Similarly, if a particular company has a large segment within a country's segment, it indicates that the company is responsible for launching a significant number of rockets in that country.
        ''')
        
        
        #--------------------------------------------------------------------------------------------     

        def plot_map(dataframe, target_column, title, width=800, height=600, color_scale='Viridis'):
            mapdf = dataframe.groupby(['country', 'alpha3'])[target_column].count().reset_index()
            fig = px.choropleth(
                mapdf, 
                locations="alpha3", 
                hover_name="country", 
                color=target_column, 
                projection="natural earth", 
                width=width, 
                height=height,
                color_continuous_scale=color_scale,
                range_color=[0, mapdf[target_column].max()],
                title=title,
                template='plotly_dark'
            )
            fig.update_geos(
                showcountries=True,
                countrycolor="white",
                showocean=True,
                oceancolor="MidnightBlue",
                showcoastlines=True,
                coastlinecolor="white",
                showland=True,
                landcolor="LightGrey"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        plot_map(
            dataframe=df, 
            target_column='Status Mission', 
            title='Number of launches per country',
            color_scale='YlOrRd'
        )

        fail_df = df[df['Status Mission'] == 'Failure']
        plot_map(
            dataframe=fail_df, 
            target_column='Status Mission', 
            title='Number of Fails per country',
            color_scale='YlOrRd'
        )  
        
        st.markdown(''' 
        ### Insights
        Insights from the chart include identifying the most active countries and companies in terms of rocket launches, as well as analyzing success rates across different countries and companies. For example, it may be possible to observe trends such as increasing involvement of private companies like SpaceX in space exploration, or the historical dominance of countries like the USA and USSR in space exploration. Additionally, by examining the mission status of launches, insights could be gained about the success rates of different rocket technologies or launch strategies.
        ''')
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Interesting Factors':
        
        data = df.groupby(['Company Name'])['Rocket'].sum().reset_index()
        data = data[data['Rocket'] > 0]

        data.columns = [
            'company', 
            'money'
        ]

        fig = px.bar(
            data, 
            x='company', 
            y="money", 
            orientation='v', 
            title='Total money spent on missions', 
            width=800,
            height=600,
            color='money',
            color_continuous_scale=px.colors.sequential.YlOrRd,
            color_continuous_midpoint=data['money'].median()
        )

        fig.update_yaxes(title='', showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)

        
        
        # #----------------------------------------------------------------------------------------
        money = df.groupby(['Company Name'])['Rocket'].sum()
        starts = df['Company Name'].value_counts().reset_index()

        starts.columns = [    'Company Name',     'count']

        av_money_df = pd.merge(money, starts, on='Company Name')
        av_money_df['avg'] = av_money_df['Rocket'] / av_money_df['count']
        av_money_df = av_money_df[av_money_df['avg']>0]
        av_money_df = av_money_df.reset_index()

        fig = px.bar(
            av_money_df, 
            x='Company Name', 
            y="avg", 
            orientation='v', 
            title='Average money per one launch', 
            width=800,
            height=600,
            color='avg',
            color_continuous_scale=px.colors.sequential.YlOrRd,
            color_continuous_midpoint=av_money_df['avg'].median()
        )

        fig.update_yaxes(title='', showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(''' 
        **Insights**
        
        The significant difference in funding between NASA and private companies reflects the different priorities and goals of each entity. NASA's focus on scientific research and pushing the boundaries of space exploration requires significant investment, which is made possible through government funding. Private companies, on the other hand, may focus more on commercial applications of space technology and therefore may not require as much funding.
        ''')
        
        #-----------------------------------------------------------------------------------------
        ds = df['year'].value_counts().reset_index()
        ds.columns = ['year', 'count']
        colors = ['#3c7ebf'] * len(ds)
        colors[0] = '#00bfff'
        bar = go.Bar(
            x=ds['year'],
            y=ds['count'],
            marker=dict(
                color=colors,
                line=dict(
                    color='#000000',
                    width=1
                )
            )
        )
        layout = go.Layout(
            title='Missions number by year',
            xaxis=dict(
                title='year',
                tickmode='linear',
                tick0=min(ds['year']),
                dtick=1
            ),
            yaxis=dict(
                title='Number of Missions',
                showgrid=True,
                gridwidth=0.5,
                gridcolor='#c0c0c0',
                tickmode='linear',
                tick0=0,
                dtick=100
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = go.Figure(data=[bar], layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('''
        **Insights**
        
        During the period between 1966 and 1978, there was a significant increase in the number of launches primarily driven by the space race between the United States and the Soviet Union. This was a period of intense competition between the two nations, and both were investing heavily in space exploration and technology development.

        In recent years, there has been renewed interest in space exploration and commercial space ventures. Private companies such as SpaceX have entered the market and are driving innovation and competition in the industry.
        ''')
        
        #-----------------------------------------------------------------------------------------
        ds = df['month'].value_counts().reset_index()
        ds.columns = [
            'month', 
            'count'
        ]
        fig = px.bar(
            ds, 
            x='month',
            y="count", 
            orientation='v', 
            title='Missions number by month', 
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #----------------------------------------------------------------------------------------
        ds = df['weekday'].value_counts().reset_index()
        ds.columns = [
            'weekday', 
            'count'
        ]
        fig = px.bar(
            ds, 
            x='weekday', 
            y="count", 
            orientation='v',
            title='Missions number by weekday', 
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #---------------------------------------------------------------------------------------
        res = list()
        for group in df.groupby(['Company Name']):
            res.append(group[1][['Company Name', 'year']].head(1))
        data = pd.concat(res)
        data = data.sort_values('year')
        data['year'] = 2020 - data['year']
        fig = go.Figure(go.Bar(
            x=data['year'],
            y=data['Company Name'],
            orientation='h',
            marker=dict(
                color=data['year'],
                coloraxis='coloraxis'
            ),
            text=data['year'],
            textposition='inside',
            hovertemplate='<b>%{y}</b><br>' +
                'Years since last start: %{x}<br>' +
                '<extra></extra>',
        ))
        fig.update_layout(
            title='Years since 2020',
            title_x=0.5,
            font=dict(size=12),
            width=900,
            height=1000,
            xaxis=dict(title='Years'),
            yaxis=dict(title='Company Name'),
            coloraxis=dict(
                colorscale='RdYlGn',
                colorbar=dict(
                    title='Years since last start',
                    titleside='right',
                    ticks='outside',
                    ticklen=5,
                    showticklabels=True
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

        #--------------------------------------------------------------------------------------
        money = df[df['Rocket']>0]
        money = money.groupby(['year'])['Rocket'].mean().reset_index()
        fig = px.line(
            money, 
            x="year", 
            y="Rocket",
            title='Average money spent by year',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #--------------------------------------------------------------------------------------
        ds = df.groupby(['Company Name'])['year'].nunique().reset_index()
        ds.columns = [    'company',     'count']
        fig = px.bar(
            ds, 
            x="company", 
            y="count", 
            title='Most experienced companies (years of launches)',
            height = 500,
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #--------------------------------------------------------------------------------------
        data = df.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()
        data.columns = [
            'company', 
            'year', 
            'starts'
        ]
        top5 = data.groupby(['company'])['starts'].sum().reset_index().sort_values('starts', ascending=False).head(5)['company'].tolist()
        data = data[data['company'].isin(top5)]
        fig = px.line(
            data, 
            x="year", 
            y="starts", 
            title='Dynamic of top 5 companies by number of starts', 
            color='company'
        )
        st.plotly_chart(fig, use_container_width=True)

        #----------------------------------------------------------------------------------------
        data = df.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()
        data.columns = [
            'company', 
            'year', 
            'starts'
        ]
        data = data[data['year']==2020]
        fig = px.bar(
            data, 
            x="company", 
            y="starts", 
            title='Number of starts for 2020', 
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)

        #------------------------------------------------------------------------------------------
        data = df[df['Status Mission']=='Failure']
        data = data.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()
        data.columns = [
            'company', 
            'year', 
            'starts'
        ]
        data = data[data['year']==2020]
        fig = px.bar(
            data, 
            x="company", 
            y="starts", 
            title='Failures in 2020', 
            width=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'The Cold war':
        st.write('This is Page 3.')
        cold = df[df['year'] <= 1991]
        cold['country'].unique()
        cold.loc[cold['country'] == 'Kazakhstan', 'country'] = 'USSR'
        cold.loc[cold['country'] == 'Russian Federation', 'country'] = 'USSR'
        cold = cold[(cold['country'] == 'USSR') | (cold['country'] == 'USA')]
        
        ds = cold['country'].value_counts().reset_index()
        ds.columns = ['country', 'count']
        colors = px.colors.qualitative.Dark24
        title_font = dict(size=20, family='Arial')
        fig = px.pie(ds, 
                    names='country', 
                    values='count', 
                    title='Number of Launches by Country',
                    hole=0.5, # Change hole size
                    color_discrete_sequence=colors, # Assign custom colors
                    labels={'country': 'Country', 'count': 'Number of Launches'}, # Rename labels
                    width=700, 
                    height=500)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(title_font=title_font)
        st.plotly_chart(fig, use_container_width=True)
        
        #----------------------------------------------------------------------------------------
        ds = cold.groupby(['year', 'country'])['alpha3'].count().reset_index()
        ds.columns = ['Year', 'Country', 'Launches']
        colors = ['rgb(53, 83, 255)', 'rgb(255, 128, 0)']
        fig = px.bar(
            ds, 
            x="Year", 
            y="Launches", 
            color='Country', 
            title='USA vs USSR: Launches Year by Year',
            color_discrete_sequence=colors, # Set custom color palette
            labels={'Year': 'Year', 'Launches': 'Number of Launches', 'Country': 'Country'}, # Rename labels
            height=500, 
            width=800
        )
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.15,
                font=dict(size=12)
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        #------------------------------------------------------------------------------------------
        import plotly.express as px
        ds = cold.groupby(['year', 'country'])['Company Name'].nunique().reset_index()
        ds.columns = ['Year', 'Country', 'Companies']
        colors = ['rgb(53, 83, 255)', 'rgb(255, 128, 0)']
        fig = px.bar(ds, 
                    x='Year', 
                    y='Companies', 
                    color='Country',
                    color_discrete_sequence=colors,
                    title='USA vs USSR: Number of Companies Year by Year',
                    labels={'Year': 'Year', 'Companies': 'Number of Companies', 'Country': 'Country'},
                    height=500, 
                    width=800)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.15,
                font=dict(size=12)
            ),
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)

        #-----------------------------------------------------------------------------------------
        ds = cold[cold['Status Mission'] == 'Failure']
        ds = ds.groupby(['year', 'country'])['alpha3'].count().reset_index()
        ds.columns = ['Year', 'Country', 'Failures']
        colors = ['rgb(53, 83, 255)', 'rgb(255, 128, 0)']
        fig = px.bar(
            ds, 
            x="Year", 
            y="Failures", 
            color='Country', 
            title='USA vs USSR: Failures Year by Year',
            color_discrete_sequence=colors, # Set custom color palette
            labels={'Year': 'Year', 'Failures': 'Number of Failures', 'Country': 'Country'}, # Rename labels
            height=500, 
            width=800
        )
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.15,
                font=dict(size=12)
            )
        )
        st.plotly_chart(fig, use_container_width=True)
               
    
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Best Every Year':
        st.write('This is Page 3.')
        ds = df.groupby(['year', 'country'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'country', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='country', 
            title='Leaders by launches for every year (countries)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #-------------------------------------------------------------------------------------
        ds = df[df['Status Mission']=='Success']
        ds = ds.groupby(['year', 'country'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'country', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='country', 
            title='Leaders by success launches for every year (countries)',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #----------------------------------------------------------------------------------------
        ds = df.groupby(['year', 'Company Name'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'company', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='company', 
            title='Leaders by launches for every year (companies)',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #---------------------------------------------------------------------------------------
        ds = df[df['Status Mission']=='Success']
        ds = ds.groupby(['year', 'Company Name'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'company', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='company', 
            title='Leaders by success launches for every year (companies)',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)



        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Time Series Decomposition':
        st.write('This is Page 3.')
        
    
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'India`s Place':
        st.write('This is Page 3.')








# Add footer
# st.markdown("""
# <style>
# .footer {
#   position: fixed;
#   left: 0;
#   bottom: 0;
#   width: 100%;
#   background-color: #f5f5f5;
#   text-align: center;
# }
# </style>
# <div class="footer">
# <p>Made with ❤️ by [Your Name]</p>
# </div>
# """, unsafe_allow_html=True)
