# We'll Look Into It

## Introduction

We'll Look Into It is designed as a county/council agnostic pothole reporting system that can be used by the public and administered by users in a council.  This initial site gives reporting capabilities and some admin features.  There is scope to develop the site further to make it even more useful to both the public and councils.

## Code Institute Milestone 3 Project

[The Live Website](https://ci-ms3-we-ll-look-into-it.herokuapp.com/)

![We'll Look Into It Logo](docs/assets/images/wlii_logo_small.png)

![mockup](docs/assets/images/mockup.png)

## Table of Contents

---

1. [Project Goals](#project-goals)
   1. [Public Users](#public-users)
   2. [Council Users](#council-users)
2. [User Experience](#user-experience)
   1. [Target Audience](#target-audience)
   2. [User Stories](#user-stories)
      1. [First Time Visitors](#first-time-visitors)
      2. [Returning Visitors](#returning-visitors)
      3. [Council Employees](#council-employees)
3. [Scope](#scope)
   1. [Design](#design)
       1. [Colour Scheme](#colour-scheme)
       2. [Typography](#typeography)
       3. [Images](#images)
4. [Wireframes](#wireframes)
5. [Features](#features)
6. [Technologies Used](#technologies-used)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Credits](#credits)
10. [Acknowledgements](#acknowledgements)

## Project Goals

### Public Users

* To have a quick and easy way to report pot holes.
* To provide comments comments when reporting a pothole.
* To see what potholes they've reported and their status.
* To delete or update the details of potholes they've reported.
* To see all potholes reported and their status.
* To be able to request re-assesment of potholes marked as no repair requied if they've gotten worse.

### Council Users

* To view a list of publicly reported potholes for assessment.
* To update the status of potholes as they progress through internal systems.
* To be able to mark potholes as resolved or not.
* To be able to grant registered users admin rights to manage potholes.
* To NOT have the ability to delete potholes, only update status.
* To see a list of newly added/unread pothole reports.
* To be able to add comments to pothole reports.

[Back to Index](#table-of-contents)

## User Experience

The site is to be designed with simplicity and ease of access in mind.  It will have a mobile first approach to make reporting potholes quick and easy.  Users will be required to register for an account to report and manage their pothole submissions.  Users will be given the opportunity to comment on their submissions to provide helpful information as to why the pothole should be dealt with.  Search capability will be provided so users, registered or not, can check if a pothole has been reported already to save duplicate reports.

### Target Audience

* Public road users
* Council employees responsible for road maintenance

### User Stories

#### First Time Visitors

As a first time visitor I want...

1. to be able to search pothole reports to see if a report has already been made.
2. to easily register for the site and submit a pothole report.

#### Returning Visitors

Upon returning to the site I want to...

3. view a list of my reports and check their status.
4. update my reports to add or remove information.
5. upvote other users reports.
6. request a previously unrepaired pothole be reviewed following a change to it's condition.

#### Council Employees

As someone administering potholes for a coucil I want to...

7. view a list of all pothole reports for my county.
8. see any newly submitted pothole reports.
9. update the status of existing reports and add comments.
10. grant access to my colleagues to be able to update reports.
11. add or update Areas for my county.
12. add or update Pothole Status'.

#### Site Owners/Administrators

As the site owner I want to...

13. have access to admin level controls.
14. add new Councils to the system.
15. set users as Admin or Master Admin.

[Back to Index](#table-of-contents)


## Scope

Based on the project goals the site will use the templating language flask so content can be built dynamically based on a backend database.  For this project MongoDB will be used for the data because of the simple data structure.

The following features will be included based on the goals and user stories.

1. Limited user management with the ability to register for a new account.
2. Create new pothole reports.
3. Search existing pothole reports.
4. Edit your own pothole reports.
5. Delete your own reports.
6. See the status of reports.

Admin features:

7. Add and remove Areas from counties.
8. Grant other users admin privileges.

Master Admin account features:

9. Add, Edit and Delete counties.
10. Add, Edit and Delete Pothole status'.
11. Revoke user admin privileges.

---

## Design

I used Materialize framework to style the site for it's range of features and Material Design styling (although this is now out of date based on Google's latest Material You style).  During development I found some limitation with the customisability of the colours used throughout the framework and it has not been updated for some years.  I will not use it in the future.

### Database

I designed the database schema to allow fo flexibility of use to be adaptable to a wide range of councils.

![image of database schema](docs/assets/images/database_schema.jpg)

### Colour Scheme

I selected a colour scheme from the range of colours provided by Materialize.  I chose a purple colour for the main theme of the site as I think this looked clean and profressional without being boring.  

To distinguish the separate data types on the site from the main data of Pothole Reports I themed the Counties, Areas and Pothole Status pages in separate colours so it is clear what area you're interacting with.

### Typography

I selelcted the Lato font for the majority of this project as it has nice round lettering and closely matches Google's Product Sans front.

### Images

The only image used on the site is the logo that I created.  It was inspired by style of the images in [this](https://www.istockphoto.com/vector/stick-figure-man-and-a-hole-on-the-floor-gm1272335094-374636205) istock image.  I created it using Google Drawings which can be found [here](https://docs.google.com/drawings/d/17fdpqD9YCwc9MGaTk4Du6HQFjLJsyXwJ5eOzAeuh3TQ/edit?usp=sharing).

### Wireframes

**Desktop**

[Potholes](docs/wireframes/d_01_home_page.jpg)

[Register](docs/wireframes/d_02_register_page.jpg)

[Login](docs/wireframes/d_03_log_in_page.jpg)

[Add Report](docs/wireframes/d_04_add_report_page.jpg)

[Manage Users](docs/wireframes/d_05_manage_users_page.jpg)

[Manage Counties, Areas or Status'](docs/wireframes/d_06_manage_county_area_status_pages.jpg)

[Add Counties, Areas or Status'](docs/wireframes/d_07_add_county_area_status_pages.jpg)

**Tablet**

[Potholes](docs/wireframes/t_01_home_page.jpg)

[Register](docs/wireframes/t_02_register_page.jpg)

[Login](docs/wireframes/t_03_log_in_page.jpg)

[Add Report](docs/wireframes/t_04_add_report_page.jpg)

[Manage Users](docs/wireframes/t_05_manage_users_page.jpg)

[Manage Counties, Areas or Status'](docs/wireframes/t_06_manage_county_area_status_pages.jpg)

[Add Counties, Areas or Status'](docs/wireframes/t_07_add_county_area_status_pages.jpg)

**Mobile**

[Potholes](docs/wireframes/m_01_home_page.jpg)

[Register](docs/wireframes/m_02_register_page.jpg)

[Login](docs/wireframes/m_03_log_in_page.jpg)

[Add Report](docs/wireframes/m_04_add_report_page.jpg)

[Manage Users](docs/wireframes/m_05_manage_users_page.jpg)

[Manage Counties, Areas or Status'](docs/wireframes/m_06_manage_county_area_status_pages.jpg)

[Add Counties, Areas or Status'](docs/wireframes/m_07_add_county_area_status_pages.jpg)

## Features

**Users**

1. Anyone can visit the site and see and search for pothole reports.
2. Members of the public can register for an account to start reporting potholes.
3. Users can edit their pothole reports.
4. Users can delete their pothole reports before they've been seen by an Admin user.
5. Users can see the status updates of their pothole reports.
6. Users cannot edit other's reports.
7. Users can upvote existing pothole reports.
8. Users can see a list of only their reports on their Profile page.

**Admins**

Admins can:

9. add comments to and set the status of reports.
0. not delete reports.
0. set registered users to be other Admins.
0. add areas to counties.
0. edit & delete areas of counties.
0. add, edit & delete pothole status'

Master Admins can:

15. perform all admin tasks above.
0. set other users as Master Admins.
0. add counties to the system.

### Future Features

- Limit upvotes to one per user.
- Admin users filter reports to their county.
- Admin users see new, unread reports.
- Admin uploads photo of fixed pothole.
- Daily digest email to Admins of potholes reported in last 24 hours in their County.
- Theme site for each County inclduing a logo
- Features to manage user's own data, update name, email, password, primary county etc.

---

## Technologies Used

### Languages
- [HTML5](https://en.wikipedia.org/wiki/CSS)
- [CSS3](https://en.wikipedia.org/wiki/CSS)
- [Javascript](https://en.wikipedia.org/wiki/JavaScript) (From W3C How To)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)

### Frameworks, libraries and other tools
[Materialize Framework](https://materializecss.com/about.html)

[Google Fonts](https://fonts.google.com/) Site fonts and icons

[Am I responsive](http://ami.responsivedesign.is/)

[VS Code](https://code.visualstudio.com/)

[git](https://git-scm.com/)

[GitHub](https://github.com/)

[Heroku](https://heroku.com/)

---

## Testing

Testing has been documented in the separate [TESTING.md](docs/TESTING.md) file

---

## Deployment

### Heroku
I have used Heroku to deploy this site.  If you would like to do the same follow these steps.
1. Within your project directory create a _.gitignore_ file & an _env.py_ file
2. Open _env.py_ and enter `import os`
3. Then set the following environment variables: 
```
os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "your unique secret key")
os.environ.setdefault("MONGO_URI", "your unique mongo db link")
os.environ.setdefault("MONGO_DBNAME", "your database name")
```
3. Add _env.py_ to the _.gitignore_ file so this senstive information is not pushed to Github
4. In a bash terminal type `pip3 freeze __local > requirements.txt`
5. Type `echo web: python app.py > Procfile` (note the capital P of Procfile)
6. Open the Procfile and remove any blank line from the bottom
7. `git add` then `git push` these files to your repository
8. Visit [heroku.com](https://www.heroku.com/) and sign in or sign up
9. Click the _New_ button > _Create new app_ in the top right
0. Enter a unique app name, this is unique to all of Heroku, not just your account
0. Select the region closest to you
0. Click _Create app_
0. Make sure you're on the Deploy tab and select GitHub from Deployment Method
0. Check that your GitHub account name is showing
0. Type part of the name of your repo to search and click _Search_
0. Click connect for the repo oyu want to connect
0. Select the Settings tab
0. Click _Reveal config vars_
0. Enter the config vars as set in your _env.py_ file above
0. Ensure that your _Procfile_ and _requirements.txt_ files are committed and pushed to GitHub
0. Return to the Deploy tab
0. Enable automatic deployments
0. Select the branch (usually main) and click Deploy Branch
0. Once the app been deployed, click on the _Open app_ tab at the top right of the page.


### Forking the GitHub Repository
If you would like to fork this respository so you can make changes without affecting the original please follow these steps:

1. Log into your GitHub account and find the [repository](https://github.com/martinbannister/CI_MS3_We-ll_Look_Into_It).
2. Click 'Fork' (last button on the top right of the repository page).
3. You will then have a copy of the repository in your own GitHub account. 

### Making a Local Clone
In order to make a clone of this repository to work on locally, follow these steps:

1. Log into your GitHub account and find the [repository](https://github.com/martinbannister/CI_MS3_We-ll_Look_Into_It).
2. Click on the 'Code' button (next to 'Add file'). 
3. To clone the repository using HTTPS, under clone with HTTPS, copy the link.
   - For SSH, click the SSH tab and copy that link.
4. Then open Git Bash.
5. Change the current working directory to where you want the cloned directory to be made.
6. In your IDE's terminal type 'git clone' followed by the URL you copied.
7. Press Enter. 
8. Your local clone will now be made.

---

## Credits

### _**Resources Used**_

These resources were used throughout the project to either directly address an issue or implement a feature.  Where appropriate (e.g the knowledge is not a general understanding) a "REFERENCE" comment has been included in the code.  Any references not included directly in the code are provided here as a reference.  

📗 **Mozialla Developer Network - Web Docs CSS**

[CSS: Cascading Style Sheets | MDN](https://developer.mozilla.org/en-US/docs/Web/CSS)

For reading up on the correct use of CSS selectors, particulary CSS Grid and shorthand properties.

📗 **W3 Schools**

[CSS Reference](https://www.w3schools.com/cssref/default.asp)

[Python Reference](https://www.w3schools.com/python/default.asp)

For reading up on and experimenting with CSS.  For python as a refresher reference to course content covered.

Specific references to creating custom Select inputs and Range inputs are included in the [style.css](../static/css/style.css) file.

📗 **Mongo DB Docs**

[Perform CRUD operations - Mongo DB Shell](https://docs.mongodb.com/mongodb-shell/crud/)

For reading up on each CRUD operation and to use non-depricated methods like those used in course content.

📗 **Flask Web Developemnt** - Developing web applications with python

Grinberg, M. (2018) _Flask Web Development_. 2nd edn. O'Reilly Media, Inc.


📗 **Reading form elements on form submit**

[https://stackoverflow.com/questions/37487826/send-form-data-to-javascript-on-submit/#57047920](https://stackoverflow.com/questions/37487826/send-form-data-to-javascript-on-submit/#57047920)

📗 **Confirming delete**

[https://stackoverflow.com/questions/45874906/flask-and-javascript-confirm-before-deleting#52675996](https://stackoverflow.com/questions/45874906/flask-and-javascript-confirm-before-deleting#52675996)

📗 **Adding labels to slider**

[https://stackoverflow.com/questions/61204680/html-range-slider-with-labels-every-5#61205099](https://stackoverflow.com/questions/61204680/html-range-slider-with-labels-every-5#61205099)

📗 **CSS Appearance property**

[https://developer.mozilla.org/en-US/docs/Web/CSS/appearance](https://developer.mozilla.org/en-US/docs/Web/CSS/appearance)

📗 **Correct use of input=range datalist labels**

[https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range#adding_hash_marks_and_labels](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range#adding_hash_marks_and_labels)

📗 **Optional parameters on flask routes**

[https://www.kite.com/python/answers/how-to-have-optional-url-parameters-using-flask-in-python](https://www.kite.com/python/answers/how-to-have-optional-url-parameters-using-flask-in-python)

📗 **Pre-populating Subject & Body in mailto: links**

[https://css-tricks.com/snippets/html/mailto-links/](https://css-tricks.com/snippets/html/mailto-links/)

### _**Acknowledgements**_

- Firstly to my Husband Graham for putting up with being lonely (yet again) whilst I spent most of my free time working on this project.
- And to my peers from the Coleg Y Cymoedd April 2021 cohort who have supported me and kept me sane, chiefly Llewelyn Williams and Andy Llewellyn.
- And to everyone on Code Institute's Slack channels who have helped and answered questions.
- Finally to Millie Kat who has been equal parts a loving companion and pest.