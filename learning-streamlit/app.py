import streamlit as st
import pandas as pd 
import plotly.express as px

st.title("Brooklyn 99 Dashboard")

#load all the datasets
df = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_episodes_cleaned.csv")
running_avg_df = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_running_avg_by_season.csv")
improvement_df = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_season_improvement.csv")
df_cult_favorite = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_cult_favorites.csv")

#adding kpis 
col1,col2,col3 = st.columns(3)

with col1:
     st.metric("Total episodes",len(df))
with col2:
     st.metric("Average show rating",df["Rating"].mean().round(2))
with col3:
     best_season = improvement_df.loc[improvement_df["improvement"].idxmax(), "Season"]
     st.metric("Best Season in terms of improvement",best_season)


st.write("Sample data")
st.dataframe(df.head(10))
st.write("Descriptive Statistics")
st.write(df.describe())

st.subheader("Rating Over Time")

#sorting the dataframe according to season and episode
df_sorted = df.sort_values(["Season","Episode"])

#creating a new column which shows episodes of each season as S<season>E<episode> format
df_sorted["season_episode"] = "S" + df_sorted["Season"].astype(str) + "E" + df_sorted["Episode"].astype(str)

#create a filter of all the charts in the dashboard
st.sidebar.header("Filters")

#create of list of seasons present in the show
seasons = sorted(df_sorted["Season"].unique())

#create a select box which shows all,1-8 seasons as selection value
selected_season = st.sidebar.multiselect("Select a Season",options=seasons,default=seasons)

#filtered dataframe
filtered_df = df_sorted[df_sorted["Season"].isin(selected_season)]
if not selected_season:
     st.warning("Please select at least one season")
     st.stop()

#create tabs for each chart
tab1, tab2, tab3 = st.tabs(["📈 Rating Trend", "📊 Season Comparison", "💎 Cult Favorites"])

with tab1:
#ordering the episode_category column
    category_order = ["Weak","Average","Great","Masterpiece"]


#creating the line chart 
    color_map = {"Weak": "#08306b", "Average": "#4292c6", "Great": "#9ecae1", "Masterpiece": "#deebf7"}
    fig = px.line(filtered_df,x="season_episode",y="Rating")
    fig.update_traces(line_color = "gray")
    fig.add_scatter(x=filtered_df["season_episode"],
                    y=filtered_df["Rating"],
                    mode="markers",
                    marker=dict(color=filtered_df["episode_category"].map(color_map), size=10),
                     text=filtered_df["Title"],
                     hovertemplate="%{text}<br>Rating: %{y}<extra></extra>",
                     showlegend=False
                    )
    
    
#fixing the x axis labels order 
    x_order = filtered_df["season_episode"].unique().tolist()

#fix the tilt of the x axis labels 
    if selected_season == "All":
        angle = 90 
    else:
        angle = -45

    fig.update_xaxes(
        categoryorder="array",
        categoryarray=x_order,
        tickangle = angle
    )

#fitting the chart to fit the container
    st.plotly_chart(fig,use_container_width=True)

with tab2:
    


#putting chart in each column
    col1,col2 = st.columns(2)

#creating a bar and a histogram
    with col1:
            st.subheader("Season Improvement")
            fig2 = px.bar(
                            improvement_df,
                            x="Season",
                            y="improvement",
                            color="improvement",
                            color_continuous_scale="Blues",
                            color_continuous_midpoint=0
    )

            st.plotly_chart(fig2,use_container_width=True)


    with col2:
            st.subheader("Rating Distribution")
            fig3 = px.histogram(df,
                                x="Rating",
                                nbins=10,
                                )
            fig3.update_layout(yaxis_title=None)
    
            st.plotly_chart(fig3,use_container_width=True)



#load the cult favorite csv

with tab3:
    
    st.subheader("Popularity vs. Appreciation")
    fig4 = px.scatter(
           df_cult_favorite,
           x="Total Votes",
           y="Rating",
           color="reception_type",
           size="Total Votes",
           hover_data=["Title", "Season", "Episode"]
       )
    st.plotly_chart(fig4, use_container_width=True)
    

