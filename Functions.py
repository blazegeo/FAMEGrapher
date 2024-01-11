def SampleTypeKey(sortedexcel):
    """Classifies as Whole Broth or Washed Broth"""
    key = []
    for x in sortedexcel.index:
        if "WB" in x:
            key.append("Whole Broth")
        else:
            key.append("Washed Broth")
    return key


def SampleNumKey(sortedexcel):
    """Counts the number of letters in the sample name"""
    num = []
    for x in sortedexcel.index:
        num.append(len(x))
    return num


def LogHour(sortedexcel):
    """Grabs the log hour from the sample name given"""
    Log = []
    for x in range(0, len(sortedexcel.index)):
        try:
            t = sortedexcel.index[x].strip().replace(",", " ").split(" ")[2]
            Time = float(t)
            Log.append(Time)
        except IndexError:
            t = 0
            Time = float(t)
            Log.append(Time)
        except ValueError:
            t = sortedexcel.index[x].strip().replace(",", " ").split(" ")[1]
            Time = float(t)
            Log.append(Time)

    return Log


def Name(sortedexcel):
    """Grabs the name only from the string"""
    name = []
    for x in range(0, len(sortedexcel.index)):
        na = sortedexcel.index[x].strip().replace(",", " ").split(" ")[0]
        name.append(na)
    return name


def Time(sortedexcel):
    """Grabs the timestamp"""
    import pandas as pd
    time = []
    for x in range(0, len(sortedexcel.index)):
        try:
            f = sortedexcel.index[x].strip().replace(",", " ").split(" ")[1].replace(".", "/")
            timestamp = pd.to_datetime(f)
            time.append(timestamp)
        except TypeError:
            timestamp = pd.to_datetime("00.00.00")
            time.append(timestamp)
    return time


def Color(sortedexcel):
    """ Inserts a randomized color for each unique name"""
    import matplotlib
    import numpy as np
    colors = dict(matplotlib.colors.cnames.items())
    hex_colors = tuple(colors.values())
    color = []
    color_d = {}
    # setting the key for each with a value that is a random color generated
    for x in sortedexcel["Name"].unique():
        color_d[x] = np.random.choice(hex_colors, replace=False)
    # Next to iterate
    for x in sortedexcel["Name"].values:
        if x in color_d:
            color.append(color_d[x])
    return color


def NaNinsert_Washed(df: list, sortedexcel: list):
    """Goal is to insert NaN values where the Name dosen't match
    df: Dataframe"""
    import numpy as np
    import pandas as pd
    # Getting the unique names and the total number of uniquw names to iterate
    unique = sortedexcel["Name"].unique()
    uni_num = len(unique)
    # the iterators
    c = 0
    # Preparing the masks
    mask = sortedexcel["Type"] == "Washed Broth"
    mask2 = sortedexcel["Name"] == unique[0]
    # Getting the NaN values to insert
    NaN = pd.Series(np.NaN)
    newlist = pd.concat((df[mask & mask2], NaN))
    while c < uni_num - 1:
        mask3 = sortedexcel["Name"] == unique[c + 1]
        newlist = pd.concat((newlist, df[mask & mask3]))
        newlist = pd.concat((newlist, NaN))
        c += 1
    newlist.set_index(["Samples"], inplace=True)
    newlist.drop(0, axis=1, inplace=True)
    return newlist


def NaNinsert_Whole(df: list, sortedexcel: list):
    """Goal is to insert NaN values where the Name dosen't match
    df: Dataframe"""
    import numpy as np
    import pandas as pd
    # Getting the unique names and the total number of uniquw names to iterate
    unique = sortedexcel["Name"].unique()
    uni_num = len(unique)
    # the iterators
    c = 0
    # Preparing the masks
    mask = sortedexcel["Type"] == "Whole Broth"
    mask2 = sortedexcel["Name"] == unique[0]
    # Getting the NaN values to insert
    NaN = pd.Series(np.NaN)
    newlist = pd.concat((df[mask & mask2], NaN))
    while c < uni_num - 1:
        mask3 = sortedexcel["Name"] == unique[c + 1]
        newlist = pd.concat((newlist, df[mask & mask3]))
        newlist = pd.concat((newlist, NaN))
        c += 1
    newlist.set_index(["Samples"], inplace=True)
    newlist.drop(0, axis=1, inplace=True)
    return newlist


def figures_to_html_nonferm(filename, filepath, progress_bar):
    '''Saves a list of plotly figures in an html file for nonferm.

    Parameters
    ----------

    filename : str
        File name to save in.

    #https://stackoverflow.com/questions/46821554/multiple-plotly-plots-on-1-page-without-subplot
    '''
    import io
    import time
    dashboard = io.open(filename, 'w', encoding="utf-8")
    dashboard.write("<html><head>"
                    "<title> FAME Grapher </title>"
                    "</head><body>" + "\n")
    dashboard.write("<h1 id = 'top'> Table of Contents </h1>"
        "<ol class = 'toc' role = 'list'>"
        "<li>"
        "<a href = '#one'>"
        "<span class = 'title'> Fat % of Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#two'>"
        "<span class = 'title'> DCW of Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#three'>"
        "<span class = 'title'> Concentration of Samples </span>"
        "</a>"
        "</li>")
    # 10% done
    progress_bar.update(1)
    time.sleep(1)
    #Grab the plots
    from Scrape import NonFermentation
    washedpercentfatty, washeddcw, washedconcentration = NonFermentation(filepath)
    #Add the Plotly Graphs with a Heading for Table of Contents
    dashboard.write("<a href = '#top'>"
        "<h1 id = 'one'> Fat % of Samples </h1>"
        "</a>")

    from Functions import fig_to_html_firstcall
    fig_to_html_firstcall(washedpercentfatty, dashboard)

    dashboard.write("<a href = '#top'>"
        "<h1 id = 'two'> DCW of Samples </h1>"
        "</a>")
    from Functions import fig_to_html
    fig_to_html(washeddcw, dashboard)
    # 30% done
    progress_bar.update_bar(3)
    time.sleep(1)

    dashboard.write("<a href = '#top'>"
        "<h1 id = 'three'> Concentration of Samples </h1>"
        "</a>")
    fig_to_html(washedconcentration, dashboard)
    # 60% done
    progress_bar.update_bar(7)
    time.sleep(1)
    dashboard.write("<footer>"
                    "<p> Code by Abdul Samateh </p>"
                    "<p><a href = 'mailto:samateh1@umbc.edu'> samateh1@umbc.edu </a></p> "
                    "</footer>")
    dashboard.write("</body></html>" + "\n")

def figures_to_html_ferm(filename, filepath, progress_bar):
    '''Saves a list of plotly figures in an html file for fermentation.

    Parameters
    ----------

    filename : str
        File name to save in.

    #https://stackoverflow.com/questions/46821554/multiple-plotly-plots-on-1-page-without-subplot
    '''
    import io
    import time
    dashboard = io.open(filename, 'w', encoding="utf-8")
    dashboard.write("<html><head>"
                    "<title> FAME Grapher </title>"
                    "</head><body>" + "\n")
    # 10% done
    progress_bar.update(1)
    time.sleep(1)
    dashboard.write("<h1 id = 'top'> Table of Contents </h1>"
        "<ol class = 'toc' role = 'list'>"
        "<li>"
        "<a href = '#one'>"
        "<span class = 'title'> Fat % of Washed Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#two'>"
        "<span class = 'title'> DCW of Washed Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#three'>"
        "<span class = 'title'> Concentration of Washed Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#four'>"
        "<span class = 'title'> Fat % of Whole Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#five'>"
        "<span class = 'title'> DCW of Whole Samples </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#six'>"
        "<span class = 'title'> Concentration of Whole Samples </span>"
        "</a>"
        "</li>")

    # Grab the plots
    from Scrape import Fermentation
    washedpercentfatty, washeddcw, washedconcentration, wholepercentfatty, wholedcw, wholeconcentration = Fermentation(filepath)
    # Add the Plotly Graphs with a Heading for Table of Contents
    dashboard.write("<a href = '#top'>"
                    "<h1 id = 'one'> Fat % of Samples </h1>"
                    "</a>")

    from Functions import fig_to_html_firstcall
    fig_to_html_firstcall(washedpercentfatty, dashboard)

    dashboard.write("<a href = '#top'>"
                    "<h1 id = 'two'> DCW of Samples </h1>"
                    "</a>")
    # 30% done
    progress_bar.update_bar(3)
    time.sleep(1)
    from Functions import fig_to_html
    fig_to_html(washeddcw, dashboard)

    dashboard.write("<a href = '#top'>"
                    "<h1 id = 'three'> Concentration of Samples </h1>"
                    "</a>")
    fig_to_html(washedconcentration, dashboard)

    dashboard.write("<a href = '#top'>"
                    "<h1 id = 'four'> Fat % of Whole Samples </h1>"
                    "</a>")
    fig_to_html(wholepercentfatty, dashboard)

    dashboard.write("<a href = '#top'>"
                    "<h1 id = 'five'> DCW of Whole Samples </h1>"
                    "</a>")
    fig_to_html(wholedcw, dashboard)
    # 60% done
    progress_bar.update_bar(6)
    time.sleep(1)
    dashboard.write("<a href = '#top'>"
                    "<h1 id = 'six'> Concentration of Whole Samples </h1>"
                    "</a>")
    fig_to_html(wholeconcentration, dashboard)

    dashboard.write("<footer>"
                    "<p> Code by Abdul Samateh </p>"
                    "<p><a href = 'mailto:samateh1@umbc.edu'> samateh1@umbc.edu </a></p> "
                    "</footer>")
    # 80% done
    progress_bar.update_bar(8)
    time.sleep(1)
    dashboard.write("</body></html>" + "\n")


def fig_to_html_firstcall(figs, dashboard):
    import plotly.offline as pyo
    """Write each figure to an html first call though, to not add extra javascript"""
    add_js = True
    for fig in figs:
        inner_html = pyo.plot(
            fig, include_plotlyjs=add_js, output_type='div'
        )

        dashboard.write(inner_html)
        add_js = False  # Saves the file from becoming bloated with javascript

def fig_to_html(figs, dashboard):
    import plotly.offline as pyo
    """Write each figure to an html"""
    add_js = False
    for fig in figs:
        inner_html = pyo.plot(
            fig, include_plotlyjs=add_js, output_type='div'
        )

        dashboard.write(inner_html)


def show_in_window(values):
    """Will be used to display the html page in its own pop up and not in browser!"""
    import sys, os
    import plotly.offline
    from PyQt6.QtCore import QUrl
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    web = QWebEngineView()
    file_path = os.path.abspath(os.path.join(os.path.dirname(values["-FILE-"]), values[0] + ".html"))
    web.load(QUrl.fromLocalFile(file_path))
    web.show()
    sys.exit(app.exec())

