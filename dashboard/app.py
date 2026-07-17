import streamlit as st
import pandas as pd 
import plotly.express as px

st.title("Brooklyn 99 Dashboard")

with st.expander("ℹ️ How to read this dashboard"):
       st.markdown("""
       This dashboard explores every episode of Brooklyn Nine-Nine using IMDb ratings and vote counts.

       - **Rating Trend**: Each episode's rating over the series, color-coded by category (Masterpiece, Great, Average, Weak). The dashed line shows the average for your current season selection.
       - **Season Improvement**: How each season's rating changed from its first to last episode.
       - **Rating Distribution**: How ratings are distributed
       - **Cult Favorites**: Episodes that were critically loved but under-watched (top-left) versus popular episodes that drew big audiences (bottom-right).
       - **Holiday vs Non-Holiday episodes**: Average rating is compared for the holiday and non-holiday episodes.

       Use the sidebar to filter by season across all tabs.
       """)

#load all the datasets
@st.cache_data
def load_episodes():
    try:
        return pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_episodes_cleaned.csv")
    except FileNotFoundError:
         st.error("Could not find b99_episodes_cleaned.csv. Check that the exports folder path is correct.")
         st.stop()

@st.cache_data
def load_running_avg():
    try:
        return pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_running_avg_by_season.csv")
    except FileNotFoundError:
         st.error("Could not b99_running_avg_by_season.csv Check that the exports folder path is correct.")
         st.stop()

@st.cache_data
def load_improvement():
    try:
        return pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_season_improvement.csv")
    except FileNotFoundError:
        st.error("Could not b99_season_improvement.csv Check that the exports folder path is correct.")
        st.stop()

@st.cache_data
def load_cult_favorite():
    try:
        return pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_cult_favorites.csv")
    except FileNotFoundError:
         st.error("Could not b99_cult_favorites.csv Check that the exports folder path is correct.")
         st.stop() 

df = load_episodes()
running_df = load_running_avg()
improvement_df = load_improvement()
df_cult_favorite = load_cult_favorite()

with st.container(border=True):
#adding kpis 
    col1,col2,col3 = st.columns(3)

    with col1:
     st.metric("Total episodes",len(df))
    with col2:
     st.metric("Average show rating",df["Rating"].mean().round(2))
    with col3:
     season_ratings = df.groupby("Season").agg(Rating=("Rating", "mean")).reset_index()
     best_season = season_ratings.loc[season_ratings["Rating"].idxmax(),"Season"]
     st.metric("Best Season",best_season)

st.divider()

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
tab1, tab2, tab3, tab4,tab5 = st.tabs(["📈 Rating Trend", "📊 Season Improvement", "📉 Rating Distribution","💎 Cult Favorites","🎄 Holiday Comparison"])

with tab1:
#ordering the episode_category column
    category_order = ["Weak","Average","Great","Masterpiece"]

#calculate avg rating across all seasons
    mean_rating = filtered_df["Rating"].mean().round(2)


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
    if selected_season == seasons:
        angle = 90
    else:
        angle = -45

    fig.update_xaxes(
        categoryorder="array",
        categoryarray=x_order,
        tickangle = angle
    )
    fig.update_layout(
    xaxis=dict(
        nticks=23,
    ))

#add average line to the graph
    fig.add_hline(
       y=mean_rating,
       line_dash="dash",
       line_color="gray",
       annotation_text=f"Average: {mean_rating}",
       annotation_position="top right"
   )


    st.plotly_chart(fig,use_container_width=True)

with tab2:
#creating a bar graph 
    filtered_improvement_df = improvement_df[improvement_df["Season"].isin(selected_season)]

    fig2 = px.bar(
    filtered_improvement_df,
    x="Season",
    y="improvement",
    color="improvement",
    color_continuous_scale="Blues",
    color_continuous_midpoint=0
)

    st.plotly_chart(fig2,use_container_width=True)
    st.caption("Season 8 shows maximum improvement")


with tab3:
    fig3 = px.histogram(filtered_df,
                        x="Rating",
                        nbins=10,
                        )
    fig3.update_layout(yaxis_title=None)
    
    st.plotly_chart(fig3,use_container_width=True)
    st.caption("A lot of the episodes have a rating between 8 to 8.4")


with tab4:
    
    filtered_cult_favorite = df_cult_favorite[df_cult_favorite["Season"].isin(selected_season)]

    fig4 = px.scatter(
       filtered_cult_favorite,
       x="Total Votes",
       y="Rating",
       color="reception_type",
       size="Total Votes",
       hover_data=["Title", "Season", "Episode"]
   )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Bubble size represents total vote count. Episodes in the top-left are critically loved but under-watched.")


with tab5:
      holiday_stats = filtered_df.groupby("is_holiday").agg(Rating=("Rating", "mean"),episode_count=("Rating", "count")).reset_index()
      holiday_stats = holiday_stats.rename(columns={'is_holiday': 'Episode Type'})
      fig5 = px.bar(holiday_stats,
                   x="Episode Type",
                   y="Rating",
                   color="Episode Type",
                   text_auto=".2f",
                   hover_data = ["Rating","episode_count"])
      st.plotly_chart(fig5,use_container_width=True)
      st.caption("Holiday Episodes on a average outperform the Non-Holiday ones")
    

