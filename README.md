# no u
suite of scripts to randomly send spam emails in gmail to those who spam you.


TO EXECUTE THIS PROGRAM:

1. Save the code to a file, for example combined_program.py.
2. Make sure you have Python 3 installed on your computer. You can check by running python --version or python3 --version in your terminal or command prompt. If you don't have Python installed, you can download it from https://www.python.org/downloads/.
3. Install the necessary packages for this program. Open a terminal or command prompt and run:

pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client schedule python-dotenv

4. Create a credentials.json file with your Google API client ID and secret, and a .env file with the following line: GMAIL_ADDRESS=your_email_address, replacing your_email_address with your Gmail address. These files should be in the same directory as combined_program.py.
5. Enable the Gmail API and People API for your Google account. Follow these instructions:

-Go to the Google API Console.
-Click "Create Project" or select an existing project.
-Use the search bar to find and enable the "Gmail API" and "Google People API".
-Go to the "Credentials" tab on the left sidebar.
-Click "Create Credentials" and select "OAuth 2.0 Client ID".
-Choose "Desktop app" as the application type.
-Download the JSON file by clicking the download icon next to your newly created  client ID, and save it as credentials.json in the same folder as combined_program.py.

6. Open a terminal or command prompt, navigate to the directory where you saved combined_program.py, and run the following command:

python combined_program.py


The program will execute, and you will be prompted to allow access to your Google account. Once authorized, the program will create the 'spammers' contact group, fetch the email addresses from the group, and schedule random emails to be sent as defined in the code. The program will keep running and executing the scheduled tasks as long as the terminal or command prompt window is open.
