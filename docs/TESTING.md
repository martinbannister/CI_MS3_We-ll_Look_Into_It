# We'll Look Into It - Testing

[Return](../README.md) to We'll Look Into It README file.

## Table of Contents

- [HTML Validation](#HTML-Validation)
- [CSS Validation](#CSS-Validation)
- [Accessibility](#Accessibility)
- [Performance](#Performance)
- [JSHint testing](#JSHint-testing)
- [Tests on Various Devices](#Tests-on-Various-Devices)
    - [Devices Tested](#Devices-Tested)
    - [Tests Performed](#Tests-Performed)
- [Testing User Stories](#testing-user-stories)
- [Browser Compatibility](#Browser-Compatibility)
- [Bugs found and resolved during development](#bugs-found-and-resolved-during-development)

---


### HTML Validation

The author used the [W3C Markup Validation Service](https://validator.w3.org/) to validate the HTML of as many of the pages on the site as possible.  Some defensive programming to prevent access to pages without being logged in made accessing them from the checker impossible.  Those pages that hadn't been locked down were manually navigated to and tested. Most pages showed no errors.

#### Login

**Login page result**

![login html result](assets/images/testing/HTML/testing_html_login.png)

#### Potholes

**Potholes list page (get_potholes)**

![get_potholes html result](assets/images/testing/HTML/testing_html_potholes_get.png)

**Pothole add page (add_pothole)**

![add_pothole html result](assets/images/testing/HTML/testing_html_pothole_add.png)

**Pothole edit page (edit_pothole)**

This page initally returned errors.

1. The 'selected' attribute had been left on the default select list option meaning when the selected option fomr the database was populated 2 options were marked as selected.
2. The 'required' attribute was included on the `input type='range'` element.  This was likely due to a copy/paste.  The author wasn't aware of this limitation until receiving this error

![edit_pothole html result with errors](assets/images/testing/HTML/testing_html_pothole_edit_errors.png)

Both these errors were corrected and a new test passed:

![edit_pothole html result corrected](assets/images/testing/HTML/testing_html_pothole_edit_fixed.png)

#### Counties

**Counties list page (get_counties)**

![get_counties html result](assets/images/testing/HTML/testing_html_counties_get.png)

**Counties edit page (edit_counties)**

![edit_counties html result](assets/images/testing/HTML/testing_html_counties_edit.png)

**Counties add page (add_counties)**

This is an example of the effect of the defensive programming at work.  Due to the page not being accessible without being logged in as a result of no session cookie present the validator was not able to access the page.

![add_counties cannot be checked error](assets/images/testing/HTML/testing_html_counties_add_defensive.png)

#### Status'
Where possible I have used the term status' to refer to multiple status items.  Where this isn't possible for programming purposes I have used statuses.  

**Status' List page (ph_status)**

![ph_status html result](assets/images/testing/HTML/testing_html_statuses_get.png)

Status add page(add_status)**

![add_status html result](assets/images/testing/HTML/testing_html_statuses_add.png)

**Status edit page (edit_status)**

![edit_status html result](assets/images/testing/HTML/testing_html_statuses_edit.png)

---

### CSS Validation

The author used the [W3C CSS Validation Service](http://jigsaw.w3.org/css-validator/validator) to validate the style.css file of the site.  It returned no errors.

![css validation result](assets/images/testing/testing_css_style.png)

---

### Accessibility

The author used the [WAVE WebAIM web accessibility evaluation tool](https://wave.webaim.org/report#/http://ci-ms3-we-ll-look-into-it.herokuapp.com/) to check if there were any issues with accessibility standards.  

The reports show some contrast errors with form labels.  These are the result of the Materialize CSS framework's predefined custom styling for input items.  This is something that I found very difficult to customise or override with my own CSS that sometimes produced inconsistent results.  As a result I have chosen to leave the form labels as they are with a view to customising in the future.

**Register page**

The register page has 6 input fields on it resulting in the 6 contrast errors.

![Register page wave result](assets/images/testing/WAVE/testing_wave_register.png)

**Login page**

![login page wave result](assets/images/testing/WAVE/testing_wave_login.png)

**Potholes list page**

![pothole page wave result](assets/images/testing/WAVE/testing_wave_potholes.png)

**Counties list page**

![counties page wave result](assets/images/testing/WAVE/testing_wave_counties.png)

---

### Performance

[Google Lighthouse](https://developers.google.com/web/tools/lighthouse/) has been used to test the performance of the main pages of the site.  For Counties, Areas and Status' the add & edit pages were not tested because these are based on the add & edit pothole pages as a starting point.

**Register**

The register page has a relatively low score on Accessibility compared to other pages.  The main difference is the use of the Materialize select input, the `label` is not associated to the `select` element using the `for` attribute which affects the score.  For a future version I will replace this with a standard `select` input with my own custom styling as used on the add and edit pothole pages.

![Lighthouse register page report](assets/images/testing/lighthouse/testing_lighthouse_d_register.png)

**Login**

![Lighthouse login page report](assets/images/testing/lighthouse/testing_lighthouse_d_login.png)

**Get Potholes**

![Lighthouse get potholes page report](assets/images/testing/lighthouse/testing_lighthouse_d_get_potholes.png)

**Add Potholes**

![Lighthouse add potholes page report](assets/images/testing/lighthouse/testing_lighthouse_d_add_pothole.png)

**Edit Potholes**

![Lighthouse edit potholes page report](assets/images/testing/lighthouse/testing_lighthouse_d_edit_pothole.png)

**Get Counties**

![Lighthouse get counties page report](assets/images/testing/lighthouse/testing_lighthouse_d_get_counties.png)

**Get Areas**

![Lighthouse get areas page report](assets/images/testing/lighthouse/testing_lighthouse_d_get_areas.png)

**Get Status'**

![Lighthouse get status page report](assets/images/testing/lighthouse/testing_lighthouse_d_get_status.png)

**Profile**

![Lighthouse profile page report](assets/images/testing/lighthouse/testing_lighthouse_d_profile.png)

**Users**

![Lighthouse users page report](assets/images/testing/lighthouse/testing_lighthouse_d_users.png)


---

### JSHint testing

The author used [JSHint](https://jshint.com/) to verify the javascript used in the site.  

In both results the undefined variable M is identified.  This is the Materialze framework's own method and is defined in an external file.

Also, both results show their respective function names as being unused variables.  These functions are called externally from HTML pages and are therefore unused within their respective scripts.

**script.js**

![main script.js JSHint results](assets/images/testing/JS/testing_jshint_script.png)

**flash_messages.js**

![flash_messages.js JSHint results](assets/images/testing/JS/testing_js_flash_messages.png)

### PEP8 Testing

The author used [PEP8 Online](http://pep8online.com/) to check the python code for any errors.  None were reported.

**PEP8 result**

![pep8 result](assets/images/testing/testing_pep8_app_py.png)


### Tests on Various Devices

#### Devices Tested

- Xiaomi Redme Note 9
- Lenovo Thinkpad C13 Yoga (Chrome & Firefox)

#### Tests Performed

1. All links in page naviagation work and aren't broken.
2. Register page works correctly and logs user in after registration.
3. Login page works.
4. Profile correctly display's users own pothole reports.
5. Potholes page shows all potholes.
6. Search function works.
7. Upvote function works.
8. Add pothole page works and pothole gets added to the database.
9. Edit pothole pages works and changes made are saved to the database.
10. Admin users can make other users Admins.
11. Master Admins users can make other users Master Admins.
12. Admins can view, edit, add & delete Areas and pothole status'.
13. Master Admins can view, edit, add & delete Counties.

### Testing User Stories

As a first time visitor I want...

1. to be able to search pothole reports to see if a report has already been made.

**Search**

https://user-images.githubusercontent.com/78867133/146532202-c3e551b8-5d07-494c-bccf-7e7c0bdbe402.mp4

2. to easily register for the site and submit a pothole report.

**Register**

https://user-images.githubusercontent.com/78867133/146469476-6b135880-9f29-4e79-8556-acae19fca975.mp4

**Add Pothole**

https://user-images.githubusercontent.com/78867133/146469623-72f9a354-5f53-4d68-ae65-6ae9df0db94d.mp4


---

Upon returning to the site I want to...

3. view a list of my reports and check their status.

https://user-images.githubusercontent.com/78867133/146532367-a6edfca1-3810-49d7-97d9-40077d6f70fd.mp4

4. update my reports to add or remove information.

**Edit**

https://user-images.githubusercontent.com/78867133/146532451-8918c791-6f7b-48f6-8682-f2e806de0d8c.mp4

**Delete**

https://user-images.githubusercontent.com/78867133/146533094-7c06e2aa-0eeb-4e6b-a0c5-a3637f1e50e5.mp4

**Read Reports Cannot Be Deleted**

https://user-images.githubusercontent.com/78867133/146533234-524e1ddb-0232-42e9-a315-18ae991018ee.mp4


5. upvote other users reports.

https://user-images.githubusercontent.com/78867133/146532525-e72fca76-10f2-4f81-9ebf-c849b80b340a.mp4

6. request a previously unrepaired pothole be reviewed following a change to it's condition.

https://user-images.githubusercontent.com/78867133/146532563-29d1846f-dd26-4b04-b743-ea71bbcc1cbd.mp4


---

As someone administering potholes for a coucil I want to...

7. view a list of all pothole reports for my county.
    - This will be made avaialable in a Future release.
8. see any newly submitted pothole reports.
    - This will be made avaialable in a Future release.
9. update the status of existing reports and add comments.

**Update Pothole Details**

https://user-images.githubusercontent.com/78867133/146469770-cadb5981-2d43-4d87-820c-f76a15a95c2c.mp4

**Pothole Marked As Read Once Opened**

https://user-images.githubusercontent.com/78867133/146533685-93b73884-3188-4aa7-8033-2e1548e2ef06.mp4


10. grant access to my colleagues to be able to update reports.

https://user-images.githubusercontent.com/78867133/146469824-419ff91e-4dfc-4125-a417-f1263ffaac5b.mp4


11. add or update Areas for my county.

**Add Area**

https://user-images.githubusercontent.com/78867133/146469851-0e2ccb06-7a97-4f9d-8814-9f09aeba65c9.mp4

**Edit Area**

https://user-images.githubusercontent.com/78867133/146469866-152cb54c-6444-440d-abea-f1d52a5c54f2.mp4

**Delete Area**

https://user-images.githubusercontent.com/78867133/146469877-42c39daa-c359-4c63-b380-bee79d36cb08.mp4

12. add or update Pothole Status'.

**Add Status**
    
https://user-images.githubusercontent.com/78867133/146281282-7fe12068-12bb-45e7-8d93-4c4561f30dd4.mp4

**Edit Status**

https://user-images.githubusercontent.com/78867133/146532871-ff245361-4909-4e3b-884c-9f8cfefdfdb5.mp4

**Delete Status**

https://user-images.githubusercontent.com/78867133/146532890-44d73abe-9a67-41d9-a9e7-ed3ec2a8a147.mp4


---

**As the site owner I want to...**

13. have access to admin level controls.

**All Admin Controls Available**

https://user-images.githubusercontent.com/78867133/146533992-c2462d46-7c74-4a9e-8f3c-ab77ff185d75.mp4


14. add new Councils to the system.

**Add Counties**

https://user-images.githubusercontent.com/78867133/146469944-942a7760-0c4a-4e4d-8eab-925630c2ed41.mp4

**Edit Counties**

https://user-images.githubusercontent.com/78867133/146469965-aee3f82e-199f-4d4c-b3aa-5f7515b1226f.mp4

**Delete Counties**

https://user-images.githubusercontent.com/78867133/146469977-0bfaf991-5546-4d51-b3a7-41a8caba79d6.mp4


15. set users as Admin or Master Admin.

https://user-images.githubusercontent.com/78867133/146469995-aed8443a-2ae4-4b65-9b23-3123765e5984.mp4



**NOTE:** Although the background image is not present in most of these vidoes it's addition had no material impact on the functionality of the site.  Performance testing was completed with the background image in place.

---

### Browser Compatibility

- Google Chrome (Desktop & Mobile)
- Mozilla Firefox
- Opera for Android

## Bugs found and resolved during development

### 🐝 **Registration form not submitting after adding validation**

- [https://stackoverflow.com/questions/22363838/submit-form-after-calling-e-preventdefault#22364136](https://stackoverflow.com/questions/22363838/submit-form-after-calling-e-preventdefault#22364136)

- Prevent default was in the wrong place.

### 🐝 **Custom select box not clickable due to overlapping icon**

![picture of custom select not working](assets/images/testing/error_custom_select.png)

- remove input-field and prefix classes, position relative and left -3.35rem, split grid into 2 columns 0px & 1fr.

### 🐝 **Delete for counties and areas not working**

- A comma was used instead of a colon in the delete_one dictionary.

### 🐝 **Delete pothole status completed without error but did not delete**

- Pothole_statuses collection was spelt incorrectly in delete_status function.

### 🐝 **Master admin switch showing for normal admin users**

- Correctly retrieved property from database, tried to retrieve only master_admin and got _id instead.  Changed users.html to reflect session_user.master_admin to correctly hide switch.

### 🐝 **Method not allowed error when updating user**

- Methods for GET and POST not specified on update_user route.

### 🐝 **Value of admin & master admin switches not saved to database**

- Names for form inputs was incorrect.  Also had to use inline if statement to convert form values to True & False respectively.

### 🐝 **Value to severity not showing on edit_pothole**

- Value attribute missing from input range on form

### 🐝 **Plus 1 icons showing twice on potholes for logged in users**

- Move second plus 1 icons to else statement of check for logged in user

### 🐝 **Admin pages remain available by url after admin log out**

- Logout did not clear session cookies for admin & master_admin

### 🐝 **Error generated when using non-existent session cookie to check user logged in**

- [https://stackoverflow.com/questions/28925602/how-can-i-detect-whether-a-variable-exists-in-flask-session/39204060](https://stackoverflow.com/questions/28925602/how-can-i-detect-whether-a-variable-exists-in-flask-session/39204060)

- Check if key exists in session first

### 🐝 **HTML checker identified required attribute on add_pothole range input**

- Removed attribute

### 🐝 **CSS validator found var(var()) in style.css**

- Removed the outer unnecessary var()


