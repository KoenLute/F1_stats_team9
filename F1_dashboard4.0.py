#!/usr/bin/env python
# coding: utf-8

# In[36]:


import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


# In[37]:


drivers = pd.read_csv("GrandPrix_drivers_details_1950_to_2022.csv")
laps = pd.read_csv("GrandPrix_fastest-laps_details_1950_to_2022.csv", sep=",", encoding="latin-1")
race = pd.read_csv("GrandPrix_races_details_1950_to_2022.csv", sep =',', encoding='latin-1')


# In[38]:


st.set_option('deprecation.showPyplotGlobalUse', False)


# In[39]:


st.set_page_config(layout='wide', initial_sidebar_state='expanded')


# In[40]:


st.sidebar.header('Dashboard `Formula 1`')

st.sidebar.subheader('Driver statistics')
selected_driver = st.sidebar.selectbox('Select a driver', drivers['Driver'].unique())


# In[41]:


st.title("Formula 1 Dashboard")


# In[42]:


# samenvoegen race en fastest laps data
merged = pd.merge(race, laps, on=["Grand Prix", "year"], how="left")


# In[43]:


# samenvoegen van data drivers
merged = pd.merge(merged, drivers[["Driver", "Nationality"]], on="Driver", how="left")


# In[44]:


# kolom toevoegen in bestand merged of de winaar ook fastest lap had
merged["Winner_is_driver"] = merged["Winner"] == merged["Driver"]


# In[45]:


# vat de data samen per decennium hoevaak winner_is_driver true of false was in %
counts = merged.groupby([(merged["year"] // 10) * 10, "Winner_is_driver"])["Winner_is_driver"].count().unstack(fill_value=0)


# In[46]:


# bereken de percentages
total = counts.sum(axis=1)
percentage = counts[True] / total * 100


# In[47]:


# bar chart maken
fig, ax = plt.subplots(figsize=(8, 6))
percentage.plot(kind="bar", ax=ax, width=0.4, position=0, label="Driver with Fastest Lap")
(100 - percentage).plot(kind="bar", ax=ax, width=0.4, position=1, color="C1", label="Other Drivers")

ax.set_title("Percentage of Races Won by Driver with Fastest Lap vs. Other Drivers, by Decade")
ax.set_xlabel("Decade")
ax.set_ylabel("Percentage of Races Won")


# In[48]:


# geef de x-as tick labels
ax.set_xticklabels([f"{i}s" for i in counts.index.get_level_values(0)], rotation=0)


# In[49]:


# legenda
ax.legend()


# In[50]:


b1, b2, = st.columns((7,5,))


# In[51]:


with b1:
    st.pyplot()


# In[52]:


# Slider per jaar voor pie chart
year = st.slider("Select a year", int(race["year"].min()), int(race["year"].max()))


# In[53]:


# filteren op jaren
data = merged[merged["year"] == year]


# In[54]:


# groepeer de data op winnaars en tel hoevaak
counts = data.groupby("Winner_is_driver")["Winner_is_driver"].count()


# In[55]:


# pie chart maken
fig2, ax2 = plt.subplots()
counts.plot(kind="pie", ax=ax2)

ax2.set_title(f"Number of Races Won by Driver with Fastest Lap vs. Other Drivers, in {year}")
ax2.legend(["Driver with Fastest Lap", "Other"])

with b2:
    st.pyplot(fig2)


# In[56]:


# filter op nationaliteit
nationality_counts = drivers.groupby("Nationality").size().reset_index(name="counts")


# In[57]:


# een altair chart maken voor nationaliteit
chart = alt.Chart(nationality_counts).mark_bar().encode(
    x="Nationality",
    y="counts",
    tooltip=["Nationality", "counts"]
).interactive()


# In[58]:


# definieer 
driver_laps = laps[laps['Driver'] == selected_driver]
driver_race = race[race['Winner'] == selected_driver]


# In[59]:


# Maak een points per season chart
points_by_season = drivers.groupby(['year', 'Driver'])['PTS'].sum().reset_index()
driver_points = points_by_season[points_by_season['Driver'] == selected_driver]

fig, ax = plt.subplots()
ax.plot(driver_points['year'], driver_points['PTS'])
ax.set_xlabel("Season")
ax.set_ylabel("Points")
ax.set_title(f"{selected_driver} Points by Season")


# In[60]:


c1, c2, = st.columns((7,5,))


# In[61]:


# Geef streamlit plek
d1, d2, d3, = st.columns((7,5,3,))


# In[62]:


with c1:
    st.altair_chart(chart, use_container_width=True)


# In[63]:


with d1:
    st.write("#### Driver Years")
    st.write(drivers[drivers['Driver'] == selected_driver])
with d2:
    st.write("#### Fastest Laps")
    st.write(driver_laps)
with d3:
    st.write("#### Driver Wins")
    st.write(driver_race)


# In[64]:


with c2:
    st.pyplot(fig)    
    


# In[65]:


# Voeg nieuwe kolom toe
drivers_laps = pd.merge(drivers, laps, on='Driver', how='outer')


# In[66]:


# voeg daar weer kolom aan toe
merged_df = pd.merge(drivers_laps, race, on='Grand Prix', how='outer')


# In[67]:


print(merged_df.head())


# In[68]:


# voeg tabellen samen
laps_race = pd.merge(laps, race, on='Grand Prix', how='outer')
laps_race.head()


# In[69]:


# Onderscheid Grand Prix namen
grand_prix_names = laps_race['Grand Prix'].unique()


# In[70]:


# Maak een sidebar
selected_gp = st.sidebar.selectbox('Select Grand Prix', grand_prix_names)


# In[71]:


# zet de sidebar op Grand Prix
filtered_df = laps_race[laps_race['Grand Prix'] == selected_gp]


# In[72]:


# Laat de winnaren zien
if filtered_df.empty:
    st.write(f"No data available for {selected_gp}")
else:
    st.write(f"Grand Prix: {selected_gp} ({filtered_df['Date'].iloc[0]})")
   

