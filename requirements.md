
## Functional Requirements
1. A visitor can create an account by providing a username, email, and password. 
2. Registered users can log in using their email and password.
3. Logged-in users can log out of their account securely.
4. Logged-in users can add new recipes with title, description, ingredients, and instructions.
5. Users can update their own recipes after creation.
6. Users can delete their own recipes.
7. Anyone can view the details of a recipe including ingredients and instructions.
8. Users can search recipes by title or ingredient keywords.
9. Users can rate a recipe from 1 to 5 stars.
10. Users can leave comments on a recipe.
11. Users can view their own profile, including their submitted recipes.
12. Users can update their display name, email, or password.
13. Users can save or 'favorite' recipes for quick access later.
14. Homepage or main recipe list shows all recipes available in the database.
15. Users can filter recipes by tags like 'vegan', 'dessert', etc.

<using the syntax [](images/ui1.png) add images in a folder called images/ and place sketches of your webpages>

## Non-functional Requirements
1. non-functional
2. non-functional

<each of the 14 requirements will have a use case associated with it>
## Use Cases <Add name of who will write (this specific requirement) and implement (in subsequent milestones) the use case below>
1. **Name:** User Registration
- **Pre-condition:** Must be on the Recipe Maker Web App website
- **Trigger:** Clicking on the Create Account button/tab
- **Primary Sequence:** 
1. User clicks text box for email
2. User types in valid email
3. User clicks text box for username
4. User types in valid username (cannot be a previously used username)
5. User clicks text box for password
6. User types in valid password
7. User clicks on submit
8. System detects if all text boxes contain valid email/username/password
9. System stores information into the database, displays text bubble to user that account created succesfully
10. System logs in User.
- **Primary Postconditions:** 
Success: The account is created and stored for further use, User is notified of the success.
Rejection: User is notified of rejection, is asked to refill information.
- **Alternate Sequence:** 
User submits invalid email/username/password
1. System detects invalid email/username/password
2. System displays text bubble to user that information is invalid, and asks to refill information
- **Alternate Sequence: 
User submits already existing account
1. System detects in database that account details/email are already being in use
2. System reloads page
3. System displays on notification bubble to user that "Account/Email already exists, please try again"

2. **Name:** User Login
- **Pre-condition:** The user is already registered in the system (i.e., has a valid email and password).
The user is not currently logged in.
- **Trigger:** The user navigates to the login page and submits their email and password through the login form.
- **Primary Sequence:** 
- 1. User navigates to the login page.
- 2. User enters their email into email box.
- 3. User enters their password into password box.
- 4. User clicks the “Login” button.
- 5. The system verifies the credentials
- 6. The system creates a session.
- 7. User is redirected to the recipe list page
- **Primary Postconditions:** 
Success: The user is logged in and has access to authenticated pages and features, and a session is securely established.
Rejection: User is notified of rejection, is asked to refill information, and a session is not established.
- **Alternate Sequence:** 
User submits invalid email/password combination
1. System detects invalid email/password
2. System displays text bubble to user that information is invalid, and asks to refill information
- **Alternate Sequence:**
No account found
1. The email entered does not match any user.
2. The system displays: “Account not found. Please register.”

3. **Name:** User Logout
Fewer than 3 primary sequence steps. 

4. **Name:** Create Recipe 
- **Pre-condition:** The user is logged in.
The user is on the “Add New Recipe” page
- **Trigger:** The user clicks “Add New Recipe” in the navigation and submits the completed recipe form.
- **Primary Sequence:** 
- 1. The user navigates to the “Add New Recipe” page.
- 2. The user fills in all required fields: Title, Description, Ingredients, Instructions.
- 3. The user clicks the “Submit” button.
- 4. The system validates the form inputs.
- 5. The recipe is saved to the database, associated with the current user.
- 6. The user is redirected to the newly created recipe’s detail page or the list of all recipes.
- **Primary Postconditions:** 
Success: A new recipe is stored in the database and is visible to the user.
Rejection: User is notified of rejection, is asked to update information.
- **Alternate Sequence:** 
Missing information
1. System detects that required fields are empty
2. System displays text bubble to user that information is missing
3. No recipe is created

5. **Name:** Edit Recipe
- **Pre-condition:** The user is logged in.
The user has already created at least one recipe.
The user is the owner of the recipe being edited.
- **Trigger:** The user clicks the “Edit” or “Update” button on one of their recipe detail pages.
- **Primary Sequence:** 
- 1. The user navigates to a recipe they previously created.
- 2. The user clicks the “Edit” button.
- 3. The system loads a form pre-filled with the current title, description, ingredients, and instructions.
- 4. The user updates one or more fields and submits the form.
- 5. The system validates the input and updates the recipe in the database.
- 6. The user is redirected to the updated recipe’s detail page.
- **Primary Postconditions:** 
Success:The user’s changes to the recipe are saved in the database, and the updated recipe is displayed with the new information.
Rejection: User is notified of rejection, is asked to update information. No changes are made to the initial recipe.
- **Alternate Sequence:** 
Missing information
1. System detects that required fields are empty
2. System displays text bubble to user that information is missing
3. Recipe remains unupdated.

6. **Name:** Delete Recipe
- **Summary:** Users can delete their own recipes. 
- **Actors:** User, System
- **Pre-condition:** The user is logged in and has a recipe saved to the database. 
- **Trigger:** The user clicks the "Delete Recipe" button on a recipe. 
- **Primary Sequence:**
- 1. The user navigates to a recipe they previously created. 
- 2. The user clicks the "Delete" button. 
- 3. The system prompts the user to confirm the deletion. 
- 4. The user confirms the deletion. 
- 5. The system deletes the recipe from the database. 
- 6. The system redirects the user to the recipe page. 
- **Alternate Sequence:** 
- 3. User does not confirm deletion. 
- a. User is then redirected to the recipe page. 
- **Post-conditions:** 
- System deletes recipe. 
- User is not able to access the deleted recipe. 

7. View Recipe 
Fewer than 3 primary sequences.

8. **Name:** Search Recipe 
- **Summary:** Users can search recipes by title or ingredient keywords.
- **Actors:** User, System
- **Pre-condition:** 
- 1. The user is logged in.
- 2. The user has recipes saved to their recipe page
- **Trigger:**: The user clicks the search bar. 
- **Primary Sequence:**
- 1. The user types the recipe name into search bar. 
- 2. The system searches the database for a matching recipe name. 
- 3. The system displays matching recipe names on the recipe page. 
- **Alternate Sequence:** 
- 2. The system does not find a matching recipe name in the database 
- 2a. The system displays a “No Recipes Found” Error. 
- **Post-conditions:** 
- The user can see recipes with a name matching with what they searched. 

9. **Name:** Rate Recipe 
- **Summary:** Users can rate a recipe from 1 to 5 stars.
- **Actors:** User, System
- **Pre-condition:** 
- 1. The user is logged in.
- **Trigger:**: The user selects the “Rate Recipe” button.
- **Primary Sequence:**
- 1. The user selects a range of star buttons corresponding to a rating from 1-5.
- 1a. 5 is a high rating, 1 is a low rating. 
- 2. The user types a review of the recipe. 
- 3. The system saves the rating into the database.
- 4. The system updates the recipe’s rating to display on the website. 
- **Alternate Sequence:** 
- 1. The user does not select a star. 
- 1a. The user may press the X button at the corner to exit the “Rate Recipe” page. 
- **Post-conditions:** 
- The recipe’s rating updates. 

10. **Name:** Comment on Recipe
- **Summary:** Users can leave comments on a recipe.
- **Actors:** User, System
- **Pre-condition:** 
- 1. The user is logged in.
- **Trigger:**: The user selects the “Comment” button.
- **Primary Sequence:**
- 1. The user types a comment into the text box.
- 2. The user selects the “Post Comment” button.
- 3. The system saves the comment into the database.
- 4. The system displays the comment on the website.
- **Alternate Sequence:** 
- 1. The user types nothing into the text box. 
- 1a. The “Post Comment” button will not appear clickable. 
- **Post-conditions:** 
- The user’s comment is displayed under the recipe.

11. View User Profile 

12. Edit User Profile 

13. Save Recipe (Favorites)

14. View All Recipes 

15. Filter Recipes 