import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go


from iso3166 import countries
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose

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
        1. Alex Tamboli - 202011071
        2. Ashish Gupta - 202011013
        3. Chinmay Badoliya - 202011016
        4. Nishesh Jain - 202011050
        5. Prashant Kumar - 202011058
        ''')
        
    
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'About Data':
        st.markdown(''' The Space Missions Analysis dataset contains information on space missions launched by various countries around the world from 1957 to present. The data includes details such as the launch date, country of origin, rocket used, mission status, and more. The dataset provides valuable insights into the history and trends of space exploration, and can be used to analyze the involvement of different countries in space missions, the success rates of missions, and the evolution of rocket technology over time. Through data visualization, this dataset can help to provide a deeper understanding of the past, present, and future of space exploration. ''')
        st.write('## Data Frame')
        st.dataframe(df)
        st.markdown("""
            ### Data Wrangling
            - TODO @Nishesh
        """)

        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Dataset Overview':
        st.write(' The higher number of rocket launches by certain countries can be attributed to a combination of historical context, technological advancements, and military applications.')
        ds = df['Company Name'].value_counts().reset_index()
        ds.columns = ['Company', 'Number of Launches']
        ds = ds.sort_values(['Number of Launches'], ascending=False)
        fig = px.treemap(ds, 
                        path=['Company'], 
                        values='Number of Launches', 
                        color='Number of Launches',
                        color_continuous_scale='YlOrRd',
                        title='Number of Launches by Every Company',
                        hover_data={'Number of Launches': ':d', 'Company': False},
                        custom_data=['Number of Launches'])
        fig.update_traces(
            hovertemplate='<br>'.join([
                'Company: %{label}',
                'Number of Launches: %{customdata[0]}'
            ]),
            hoverlabel=dict(
            bgcolor="yellow",
            font=dict(size=12, color = "black")
            ),
            marker=dict(cornerradius=15)
        )
        fig.update_layout(height = 400,
                          margin = dict(t=50, l=25, r=25, b=2))
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
                font=dict(size=20)
            ),
            margin=dict(l=0, r=0, t=50, b=0),
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
                    height=500, 
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
            ),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
         The high success rates of missions were likely due to a combination of technological advancements, rigorous testing and quality control procedures, experience and expertise, and strategic importance.

        ''')

        #------------------------------------------------------------------------------------
        fig = go.Figure(go.Histogram(
            x=df['Rocket'],
            nbinsx=50
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
            height=500 
        )
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(''' 
        ### Insights
          The disparity in the number of launches by the USSR and the US compared to other countries can be attributed to a combination of early development, budgetary constraints, technology transfer, and international cooperation. However, in recent years, other countries like China, India, and Japan have been investing heavily in their space programs and are catching up in terms of the number of launches and achievements in space exploration.
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
        st.markdown(''' 
        ### Insights
        A world heat map that shows the number of space missions by country can provide valuable insights into the distribution of space exploration activity around the world.In this case, the map shows that the USSR and the US have had significantly more space missions than other countries.However, the map also shows that other countries like China, India, and Japan are becoming increasingly active in space exploration and are catching up to the US and the USSR in terms of the number of missions. 
        ''')

        fail_df = df[df['Status Mission'] == 'Failure']
        plot_map(
            dataframe=fail_df, 
            target_column='Status Mission', 
            title='Number of Fails per country',
            color_scale='YlOrRd'
        )  
        st.markdown(''' 
        ### Insights
        The higher success rate of the USSR's space program may have been due to a combination of factors, including factors such as

        1.The Soviet Union's space program was often characterized by a focus on simplicity and reliability.

        2.The Soviet Union was known for placing a high priority on the safety of its cosmonauts and spacecraft.

        3.The Soviet Union invested heavily in its launch infrastructure, building a network of launch facilities and associated infrastructure that could support a wide range of missions.

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
            height=500,
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
            height=500,
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
        st.write('There is no clear pattern in terms of which days and month have more or fewer launches. Lack of dependence on the month and weekdays may be due to the fact that space agencies and companies have a relatively consistent schedule of launches throughout the year which includes careful planning, preparation, and monitoring to ensure a safe and successful launch.')
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
            title='Years since last Rocket launch from 2020',
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
        fig.update_layout(
            yaxis_title='Money'
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
            title='Top 5 companies by number of launches', 
            color='company'
        )
        fig.update_layout(
            yaxis_title='Launches'
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
        st.write(' During the Cold War, the United States and the Soviet Union were engaged in intense competition across a wide range of areas, including space exploration. The Cold War between the United States and the Soviet Union had a significant impact on space exploration, driving a rapid advancement in space technology and an increase in space-related investments. Both countries saw space exploration as a way to demonstrate their technological and military superiority and to gain an advantage over the other.')
        st.write('Overall, the Cold War period saw a significant increase in the number of rockets launched and successful space missions by both the United States and the Soviet Union. ')
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
        st.write('The Cold War period saw a total of 2,332 successful space missions by both the United States and the Soviet Union. These missions included those related to satellite launches, human spaceflight, and planetary exploration.')
        
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
        st.markdown('''
        Between 1957 and 1991, the Soviet Union launched a total of 1770 rockets, including those for military and civilian purposes.The Soviet Union also had several successful missions to the Moon and developed a number of key space technologies, such as space stations and interplanetary probes.

        Between 1958 and 2011, the United States launched a total of 1,736 rockets, including those for military and civilian purposes. The United States achieved several major milestones during the Cold War period, such as the successful landing of astronauts on the Moon and the development of the Space Shuttle program.
        ''')

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
        st.markdown('''
        The fluctuations in the number of companies in both countries could also be due to changes in government policies or economic factors, which can have an impact on the funding and support available for space exploration.

        The US has a strong history of investing in space exploration through NASA and private companies like SpaceX and Blue Origin. This has led to more companies involved in space exploration in the US than in other countries. However, changes in government policies and economic factors can impact the number of companies involved.
        
        On the other hand, the number of companies involved in space exploration in the Soviet Union was more limited, with most space-related activities being controlled by the government. This could be a reason why the number of companies involved in space exploration in the Soviet Union did not increase as rapidly as in the US.
        ''')

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
        st.write(''' Overall, the higher success rate of the USSR's space program may have been due to a combination of factors-''')
        st.write("1. The US was playing catch-up to the Soviet Union, which had achieved several milestones before the US, such as launching the first satellite (Sputnik) and sending the first human (Yuri Gagarin) into space. As a result, the US was under pressure to make rapid progress in space exploration, which led to some rushed and risky decisions.")
        st.write("2. Secondly, the US was pushing the boundaries of technology and science in ways that had not been done before. This meant that there were more opportunities for things to go wrong.")
        st.write("3. Thirdly, there were technical challenges with the early American rockets, particularly the early versions of the Saturn rockets, which were prone to failures. ")
    
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
