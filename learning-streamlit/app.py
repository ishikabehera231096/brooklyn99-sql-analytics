import streamlit as st
import pandas as pd 
import plotly.express as px

st.title("Brooklyn 99 Dashboard")

df = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_episodes_cleaned.csv")
st.write(f"Loaded {len(df)} episodes")
st.dataframe(df.head(10))
st.write(df.describe())

st.subheader("Rating Over Time")

#sorting the dataframe according to season and episode
df_sorted = df.sort_values(["Season","Episode"])

#ordering the episode_category column
category_order = ["Weak","Average","Great","Masterpiece"]

#creating a new column which shows episodes of each season as S<season>E<episode> format
df_sorted["season_episode"] = "S" + df_sorted["Season"].astype(str) + "E" + df_sorted["Episode"].astype(str)
seasons = sorted(df_sorted["Season"].unique())

#create a select box which shows all,1-8 seasons as selection value
selected_season = st.selectbox("Select a Season",options=["All"]+list(seasons))

#creating a logic for selection critrea
if selected_season != "All":
    filtered_df = df_sorted[df_sorted["Season"] == selected_season]
else:
    filtered_df = df_sorted

#creating the line chart 
fig = px.line(filtered_df,
              x="season_episode",
              y="Rating",
              color="episode_category",
              category_orders={"episode_category":category_order},
              hover_data=["Title"],
              title="Every Episode Rated",
              markers=True)

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


# loading the season improvemement csv
improvement_df = pd.read_csv("/Users/ishik/Desktop/brooklyn99-sql-analytics/exports/b99_season_improvement.csv")


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
            fig3 = px.histogram(filtered_df,
                                x="Rating",
                                nbins=10,
                                )
            fig3.update_layout(yaxis_title=None)
    
            st.plotly_chart(fig3,use_container_width=True)



#load the cult favorite csv
