# State Senate Topic Analysis and Dashboard
### Metis Final Project - June 2018

Welcome to my New York State Senate topic analysis project and visualization Dashboard.

For my final project at Metis, I wanted to work with public data to help make local government more transparent and understandable. To do so, I downloaded 133K bills in the New York State Legislature via their OpenData Portal. I also combined this with topic analysis of the New York Times coverage of the NY State Senate, primarily to see if the area's most famous newspaper accurately mirrored policy priorities.

You can read more about my process [here](https://bnewborn.github.io/BNewborn.github.io/2018/07/05/Increasing-Transparency-in-Albany.html) in my data science blog.

A quick summary of the notebooks is below:

* Notebooks labeled "1_" and "2_" were the API pulls from each source
* 3-6 were cleaning and topic analysis of the Times data
* Folder "7_senateclean" features cleaning the dense Senate data. The reason for splitting this out is that each area of information for a given bill was given as a dictionary. So I used separate notebooks to carefully split each dictionary open into a row, and then joined them together at the end via a common index.

Notebooks 8 and 9 are topic analysis of the resulting clean corpus of Senate bills.

I created a visualization via Dash to help users understand and extract value from all of this work.

[Link to Dashboard](http://bnsenatefinal-env.qtqc42jatv.us-east-1.elasticbeanstalk.com/)
*Note - dashboard has been removed due to AWS Restrictions. A demo video of the dashboard can be seen [here](https://vimeo.com/278546669)

I then presented these findings to Metis' career night on the evening of Thursday, June 28. My slides are uploaded here as [Keynote Presentation.pdf](/Keynote_Presentation.pdf)
