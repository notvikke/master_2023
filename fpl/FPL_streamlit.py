import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Podium function
def display_podium(title,df,column=1,value="pts"):
    st.subheader(title)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image("pictures/{}.png".format(df.loc[0, "manager"])) 
        st.subheader("🥇")
        st.text("{}: {} {}".format(
            df.loc[0, "manager"], 
            round(df.iloc[0, column]),
            value))

    with col2:
        st.write("")
        st.write("")
        st.image("pictures/{}.png".format(df.loc[1, "manager"]))
        st.subheader("🥈") 
        st.text("{}: {} {}".format(df.loc[1, "manager"], round(df.iloc[1, column]),value))

    with col3:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.image("pictures/{}.png".format(df.loc[2, "manager"]))
        st.subheader("🥉") 
        st.text("{}: {} {}".format(df.loc[2, "manager"], round(df.iloc[2, column]),value))

    with col4:
        st.write("")

    with col5:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.image("pictures/{}.png".format(df.loc[len(df)-1, "manager"]))
        st.subheader("💩",)
        st.text("{}: {} {}".format(df.loc[len(df)-1, "manager"], round(df.iloc[len(df)-1, column]),value))

def show_pics(data,num, points=False):
    st.image("https://resources.premierleague.com/premierleague/photos/players/110x140/p{}.png".format(data.loc[num,"photo"]))
    if data.loc[num,"player_id"]==32:
        st.markdown("{} ✅".format(data.loc[num,"player_name"]))
    else:
        st.markdown("{}".format(data.loc[num,"player_name"]))
    
    st.markdown("{} gameweeks".format(data.loc[num,"player_id"]))

    if points=="total":
        st.success("{} points total".format(data.loc[num,"points"]))
    elif points=="average":
        st.success("{} points per game".format(round(data.loc[num,"points"]/data.loc[num,"player_id"],2)))

def points():
    # Basic text elements in streamlit
    st.header("This is a header")
    st.subheader("This is a subheader")
    st.text("This is a text")
    st.markdown("This is a **markdown** text")
    st.code("# This is code\ndata = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})")

    # Status elements
    st.success("This is a success")

    st.warning("This is a warning")

    # region Final Standings

    st.header("Akoya FPL Award")
    st.markdown("A little jacking off session to the ones that got the most points overall")
    main_ranking = pd.read_csv('findings/points/real_ranking.csv')

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=main_ranking['manager'],
        y=main_ranking["points"],
        name='Final Standings'
    ))

    # Update the layout of the chart
    fig.update_layout(
        title='Final Standings',
        xaxis_title='Managers',
        yaxis_title='Points'
    )

    tab1, tab2 = st.tabs(["Top 3", "Table"])

    # Create a tab for the pictures
    with tab1:
        display_podium("Final Standings Top 3",main_ranking)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Final Points")
        st.write(main_ranking)

    #endregion
    
    st.info("But we already knew that.")
    st.info("Let's look a bit deeper into some of the choices made in these past few months...")
    st.header("Rankings per Position")

    # region Goalkeeper Rankings
    st.subheader("Goalkeepers")
    st.markdown("A useless award for the most brain dead position in fpl. Pick a top 6 gk and inshallah.")

    data = pd.read_csv('findings/points/gk_ranking.csv')
    data_gw = pd.read_csv('findings/points/gw_gk_ranking.csv')

    tab1, tab2, tab3, tab4 = st.tabs(["Top 3", "Table", "Best Gameweek", "GW Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Goalkeeper Standings Top 3",data)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Goalkeeper Points")
        st.write(data)

    with tab3:
        display_podium("Goalkeeper Best Gameweek Top 3",data_gw,2)

    with tab4:
        st.subheader("Table of Goalkeeper Best Gameweeks")
        st.write(data_gw)
    # endregion

    # region Defender Rankings
    st.subheader("Defenders")
    st.markdown("A single goal vs Arsenal can mean 4 points for someone. But it also means Ruslan losing 16 cleansheet points")

    data = pd.read_csv('findings/points/def_ranking.csv')
    data_gw = pd.read_csv('findings/points/gw_def_ranking.csv')

    tab1, tab2, tab3, tab4 = st.tabs(["Top 3", "Table", "Best Gameweek", "GW Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Defender Standings Top 3",data)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Defender Points")
        st.write(data)

    with tab3:
        display_podium("Defender Best Gameweek Top 3",data_gw,2)

    with tab4:
        st.subheader("Table of Defender Best Gameweeks")
        st.write(data_gw)
    # endregion

    # region Midfielder Rankings
    st.subheader("Midfielders")
    st.markdown("CDMs are the cucks of Fantasy, might as well put a disabled person instead")
    data = pd.read_csv('findings/points/mid_ranking.csv')
    data_gw = pd.read_csv('findings/points/gw_mid_ranking.csv')

    tab1, tab2, tab3, tab4 = st.tabs(["Top 3", "Table", "Best Gameweek", "GW Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Midfielders Standings Top 3",data)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Midfielder Points")
        st.write(data)

    with tab3:
        display_podium("Midfielder Best Gameweek Top 3",data_gw,2)

    with tab4:
        st.subheader("Table of Midfielder Best Gameweeks")
        st.write(data_gw)
    # endregion

    # region Forward Rankings
    st.subheader("Forwards")
    st.markdown("The most prestigious award. Specially the Best Gameweek section")

    data = pd.read_csv('findings/points/fwd_ranking.csv')
    data_gw = pd.read_csv('findings/points/gw_fwd_ranking.csv')

    tab1, tab2, tab3, tab4 = st.tabs(["Top 3", "Table", "Best Gameweek", "GW Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Forwards Standings Top 3",data)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Forward Points")
        st.write(data)

    with tab3:
        display_podium("Forward Best Gameweek Top 3",data_gw,2)

    with tab4:
        st.subheader("Table of Forward Best Gameweeks")
        st.write(data_gw)
    # endregion

    st.info("Haaland was 221 of those points btw")
    st.info("Anyways, some highs, some lows... but all our own choices, for the most part")
    st.info("Now let's look at the ones we didn't choose, let's look...")
    st.header("Outside the starting 11")

    # region Bench FC
    st.subheader("Bench FC")
    st.markdown("Ranking of teams with most points in their bench")
    data = pd.read_csv('findings/points/bench.csv')

    tab1, tab2 = st.tabs(["Top 3", "Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Bench FC Standings Top 3",data)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Bench Points")
        st.write(data)
    # endregion

    # region Optimised Bench
    st.subheader("Optimised Bench")
    st.markdown("Basically a 'What if...?' in which we look at how many points were left on the bench everyone except Yahya could have capitalised on")
    data = pd.read_csv('findings/points/bench_best.csv')

    merged_df = pd.merge(data, main_ranking, on='manager')
    merged_df['Final Points'] = merged_df['points_x'] + merged_df['points_y']
    result_df = merged_df[['manager', 'Final Points']].sort_values(by='Final Points',ascending=False)

    trace2 = go.Bar(
        x=merged_df["manager"],
        y=merged_df["Final Points"],
        name='Optimised Points',
        marker=dict(color='blue')  # Set the color for the bars of Series 1
    )

    # Create a bar trace for the second series
    trace1 = go.Bar(
        x=main_ranking["manager"],
        y=main_ranking["points"],
        name='Final Ranking',
        marker=dict(color='green')  # Set the color for the bars of Series 2
    )

    # Create the data list with both traces
    data2 = [trace1, trace2]

    # Define the layout
    layout = go.Layout(
        title='Comparison of Final Ranking vs Optimised Points',
        xaxis=dict(title='Manager'),
        yaxis=dict(title='Points')
    )

    # Create the figure
    fig = go.Figure(data=data2, layout=layout)

    tab1, tab2, tab3 = st.tabs(["Top 3", "Table", "Updated Final Standings"])

    # Create a tab for the podium
    with tab1:
        display_podium("Optimised Bench Standings Top 3",data)

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Missed Bench Points")
        st.write(data)

    with tab3:
        st.subheader("Table of Optimised Points vs Final Ranking")
        st.plotly_chart(fig)
    # endregion

    st.info("De Bruyne in the bench was a brave choice")
    st.info("Since we've looked at our points and our choices, let's look at what we saw in the end of every gameweek. Let's look at...")
    st.header("Gameweek Winners and Losers")

    # region Podiums
    st.subheader("Podiums")
    st.markdown("Amount of times in the top 3 each gameweek")
    data = pd.read_csv('findings/points/podiums.csv')

    first = data[["manager","1st"]].sort_values("1st",ascending=False).reset_index(drop=True)
    second = data[["manager","2nd"]].sort_values("2nd",ascending=False).reset_index(drop=True)
    third = data[["manager","3rd"]].sort_values("3rd",ascending=False).reset_index(drop=True)
    total = data[["manager","Total"]].sort_values("Total",ascending=False).reset_index(drop=True)

    tab1, tab2, tab3, tab4, tab5= st.tabs(["First Place", "Second Place", "Third Place", "Total Podiums", "Table"])


    # Create a tab for the podium
    with tab1:
        display_podium("1st Place Gameweeks",first,1, "gws")

    with tab2:
        display_podium("2nd Place Gameweeks",second,1, "gws")
    
    with tab3:
        display_podium("3rd Place Gameweeks",third,1, "gws")
    
    with tab4:
        display_podium("Total Podiums",total,1, "gws")

    # Create a tab for the table
    with tab5:
        st.subheader("Table of Podiums")
        st.write(data)

    
    # endregion

    # region Tottenham
    st.subheader("Tottenham Award")
    st.markdown("A tribute to the chickens, a ranking of the longest streaks without winning a podium in the league")
    data = pd.read_csv('findings/points/tottenham.csv')

    tab1, tab2 = st.tabs(["Top 3", "Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Longest Winless Streak Top 3",data,1,"gws")

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Longest Winless Streak")
        st.write(data)
    # endregion

    # region Last Place
    st.subheader("Last Places")
    st.markdown("Pretty self explanatory... a ranking of Last Place gameweek Finishes")
    data = pd.read_csv('findings/points/last_df.csv')

    tab1, tab2 = st.tabs(["Top 3", "Table"])

    # Create a tab for the podium
    with tab1:
        display_podium("Last Places Top 3",data,1,"gws")

    # Create a tab for the table
    with tab2:
        st.subheader("Table of Last Places")
        st.write(data)
    # endregion

    # region other
    # get data to display
    data = px.data.iris()
    st.markdown("We also can include dynamic tables with `st.dataframe`")
    st.dataframe(main_ranking.head())
    st.markdown("And also static tables with `st.table`")
    st.table(main_ranking.head())
    st.markdown("And also metrics with `st.metric` combined with `st.columns`")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    st.markdown("Including plotly plots with `st.plotly_chart`")
    st.plotly_chart(
        px.scatter(
            data, x="sepal_width", y="sepal_length", color="species", template="none"
        )
    )

    st.markdown("Including images with `st.image`")
    st.image("https://media.giphy.com/media/zGnnFpOB1OjMQ/giphy.gif", caption="My image")

    st.markdown("Including video with `st.video`")
    st.video("https://youtu.be/5-tHimysW-A")

    with st.container():
        st.markdown(
            "Including widgets with `st.button`, `st.checkbox`, `st.radio`, `st.selectbox`, `st.slider`, `st.text_input`, `st.text_area`, `st.date_input`, `st.time_input`"
        )
        st.button("This is a button")
        st.checkbox("This is a checkbox")
        st.radio("This is a radio", ("Option 1", "Option 2"))
        st.selectbox("This is a selectbox", ("Option 1", "Option 2"))
        st.slider("This is a slider", 1, 100)
        st.text_input("This is a text input")
        st.text_area("This is a text area")
        st.date_input("This is a date input")
        st.time_input("This is a time input")

        st.markdown("Including progress bars with `st.progress`")
        my_bar = st.progress(0)
        for p in range(10):
            my_bar.progress(p + 1)

        st.markdown("Or a spinner with `st.spinner`")
        with st.spinner("Wait for it..."):
            time.sleep(1)
        st.success("Done!")


    st.markdown("Separating views in different tabs with `st.tabs`")
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    data = np.random.randn(10, 1)

    tab1.subheader("A tab with a chart")
    tab1.line_chart(data)

    tab2.subheader("A tab with the data")
    tab2.write(data)

    st.markdown("This is a form with `st.form`")
    with st.form("my_form"):
        st.write("Inside the form")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)

    # Retrieve location data
    st.markdown("This is a map with `st.map`")
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
    )

    st.map(df)


    # Also, we can include those elements in the sidebar
    st.sidebar.title("Including things also in a sidebar!")
    st.sidebar.button("This is a sidebar button")
    st.sidebar.checkbox("This is a sidebar checkbox")
    st.sidebar.radio("This is a sidebar radio", ("Option 1", "Option 2"))
    st.sidebar.selectbox("This is a sidebar selectbox", ("Option 1", "Option 2"))
    st.sidebar.slider("This is a sidebar slider", 1, 100)
    st.sidebar.text_input("This is a sidebar text input")
    st.sidebar.text_area("This is a sidebar text area")
    st.sidebar.date_input("This is a sidebar date input")
    st.sidebar.time_input("This is a sidebar time input")
    #endregion

def players():
    st.subheader("Players Page")
    st.markdown("Some individual and group facts about players in the AKOYA league. Please choose a manager in the sidebar")

    st.sidebar.markdown("Choose a manager")
    manager = st.sidebar.selectbox("Choose Manager", ("Ali","Ruslan","Sami","Yahya","Youssef","Santi","Shrey","Dani"))

    st.markdown(" ")
    st.info("Choosing who to have in your team was hard, unless you just chose Arsenal players and called it a day")
    st.info("Let's first look at who has stuck with you through thick and thin, and ask yourself why Ali was such a lucky bitch for getting Haaland as his first pick. Let's look at...")
    st.header("Loyalty")
    st.markdown("The players you've owned the longest")

    #region Loyalty
    data = pd.read_csv('findings/players/loyalty.csv')

    manager_df = data[data["manager"]==manager].sort_values("player_id",ascending=False).reset_index(drop=True).iloc[:10]
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            show_pics(manager_df,i)
            show_pics(manager_df,i+5)
    #endregion
    
    st.header("UnLoyalty")
    st.markdown("The opposite of the last one")

    #region Unloyalty?
    manager_df = data[data["manager"]==manager].sort_values("player_id",ascending=True).reset_index(drop=True).iloc[:10]
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            show_pics(manager_df,i)
    #endregion

    st.header("Most Played")
    st.markdown("The players you've fielded the most")

    #region Most Played
    data = pd.read_csv('findings/players/most_played.csv')
    manager_df_full = data[data["manager"]==manager].reset_index(drop=True).sort_values("player_id",ascending=False)
    manager_df = manager_df_full[:10]
    tab1, tab2 = st.tabs(["Points Total","Points per Game"])

    with tab1:
        tab1_cols = st.columns(5)
        for i in range(5):
            with tab1_cols[i]:
                show_pics(manager_df,i,"total")
                show_pics(manager_df,i+5,"total")
                
    with tab2:
        tab2_cols = st.columns(5)
        for i in range(5):
            with tab2_cols[i]:
                show_pics(manager_df,i,"average")
                show_pics(manager_df,i+5,"average")

    #endregion
    
    st.info("We've seen the players that have been most in ONE team, now let's look at the players that have been in MOST teams")

    st.header("Most Teams")
    st.markdown("What I just said")

    #region Most Teams
    most_teams = pd.read_csv('findings/players/most_teams.csv')[:8]

    cols = st.columns(4)

    for i in range(4):
        with cols[i]:
            st.image("https://resources.premierleague.com/premierleague/photos/players/110x140/p{}.png".format(most_teams.loc[i,"photo"]))
            st.markdown("{}".format(most_teams.loc[i,"player_name"]))
            st.markdown("in {} teams".format(most_teams.loc[i,"0"]))    


            if most_teams.loc[i,"player_name"] in manager_df_full["player_name"]:
                row = manager_df_full[manager_df_full["player_name"]==most_teams.loc[i,"player_name"]]
                st.markdown("{} gameweeks in your team".format(row["player_id"]))
                st.success("{} points total".format(row["player_id"]))
    #endregion


def stats():
    st.subheader("Genneral Statistics Page")
    st.markdown("Summary of general statistics relating to the AKOYA league")

def transfers():
    st.subheader("Transfers Page")
    st.markdown("Quick view of the best and worst transactions in the AKOYA league")

pages = {
    "Points": points,
    "Players": players,
    "General Stats" : stats,
    "Transfers" : transfers
}

# Streamlit app
def main():
    st.title("AKOYA FPL Draft Wrapped")
    st.markdown("Let's look back at this season")
    multiline_text = """\n
    Please navigate this Akoya Wrapped with the sidebar.\n
    You can choose between four types of insights:\n
    'Points', 'Players', 'Stats', and 'Trades'"""
    st.info(multiline_text)

    # Add sidebar navigation
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Call the function based on selection
    pages[selection]()  


if __name__ == "__main__":
    main()