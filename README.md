
This program is a grapher of the percent fat and concentrations of compounds found in FAME analysis for all samples depending on which department they were recieved from, in this case Fermentation or Non-Fermentation.
It was made to minimize the time spent manually creating a graph for each subset of samples which took more time as sample size increased in size and complexity of batch composition.
In using this grapher program, one should be able to recieve a visual representation of the processed data from Chromeleon and make decisions on whether to return to processing or note trends in a quicker turnaround time.

By making this program I've learned the various ways that syntax with sample names differs between departments and the extra work needed to incorporate a user-end experience as I've only worked solely on functions for my own use locally, making this a good start into the world of python development.
								
						       --FAME GRAPHER How-To:--

1. Open the file containing the Fame Grapher executable
2. The excel sheet named FAME Graph Checker will be where the processed data from Chromeleon or another report will be pasted.
--NOTE: There are no spaces between the Percentages and the Concentration so mind for that if pasting from a report that seperates them--
3. Take the Sample Name and FAME Data and paste into the respective rows. The Dry Cell Weight(DCW) can be found from the 
Fame Weights sheet but if not given that row can be populated with 1s or 0s to minimize errors.
4. Once the data is all there, open the Fame Grapher executable. You will be greeted by the FAME Sheet Locator accompanied with a Browse button,
a choice box asking whether the FAME data is from Fermentation or Non-Fermentation and what you want the name of your output html to be.
						 
						 Executable User-End Screen Guide:
5a. The Fame Sheet Locator can be directed to the FAME grapher sheet as that is where we've set up our data.
5b. The FAME data is from Fermentation if the syntax of the sample name follows Name/Date/LogHour(Ex: B5 08.25.23,11) or Name/LogHour(Ex: 223PBCF018 0) if it dosen't it is classified as Non-Fermentation for the code's purposes.
5c. The name of the output HTML was be advised to be the name of the FAME run but can be whatever it needs to be.
--NOTE: The program creates an html in order to have interactable graphs, opening them only requires using your browser of choice
once they are created in the directory of the program.
 
6. Once you have entered all your information you can press "Execute" and wait up to a minute and a pop-up window containing the graphs will appear.
7. If you chose the FAME data to be Fermentation:
Graphs displayed will be Percentages and Conecentrations of Compounds of Washed Broth Samples plus Dry Cell Weights then same for Whole Broth Samples.
8. If you chose the FAME data to be non-Fermentation:
Graphs displayed will be Percentages and Concentrations of Compounds + Dry Cell Weights for the samples.
--NOTE: The output file will be created in the same directory of the executable so can be opened from there or anywhere you move it once located. --


						    ---Features of the Graphs---

				-This will be from left to right describing the buttons found on the top right of each graph-

Camera: This will download a png image of the current plot, it will not have the interactivity but will be a static image. Will need the html to be opened in
your browser to find the png in your downloads folder. Might be an issue with the webbrowser produced by Python.

Select Tools (These four options can only be active one at a time, they affect how you interact with the graph with your cursor):
Zoom) A click and drag will zoom in the graph at the area you encompass
Pan) A click and drag will move the points of the graph within the scale and will be how you generally move around when zoomed in.
Box Select) A click and drag will highlight a box of the graph and only the points within the box will appear colored. Can be
canceled by double-clicking outside the box.
Lasso Select) A click and drag will allow a freeform area of the graph to be signled out and highlighted. Can be canceled by
double-clicking outside the box.

Zoom In: Will zoom in the scale on all sub-plot graphs within the figure.
Zoom Out: Will zoom out the scale on all sub-plot graphs within the figure.
Autoscale & Reset Axes: These will both reset the view of each graph back to when they were first viewed and defaulted as.
Usually good enough to see the trends at first glance.

							       Legend:

We will find our legend on the very right of our graphs and they will display the color of the line with a circle marker in the middle, followed by the name of what that line represents.

By single-clicking any of those line-circle symbols you can remove the line from its respective graph, it can be added again
by single-clicking again.

By double-clicking any of the line-circle symbols you can isolate the graph to only display only that line for the entire figure,
which helps when you want to minimize noise from other figures. Double-clicking again cancels out this isolation.

Through combinations of the two you can customize what you want displayed on the figure and help hone in on trends you want to analyze.

							Known Issues:

If you have your files synced with onedrive, most likely the application won't work. In order to fix this, Open up File Explorer, Click Local Disk, Go to Users, Go to XXXXX (which will be numbers unique to your DSM computer),
there you can go to Documents and move all the files associated with the FAMEGrapher there prefereably in a single file. Now when you use the program, the FAME excel sheet is no longer being synced with OneDrive and won't fail.


