import firebase_admin
from firebase_admin import credentials, auth, db
import json
import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Initialize Firebase Admin
cred = credentials.Certificate(
    "mentalmath-17de2-firebase-adminsdk-fbsvc-6e684271b1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mentalmath-17de2-default-rtdb.firebaseio.comhttps://mentalmath-17de2-default-rtdb.firebaseio.com'
})

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile("mycreds.txt")
elif gauth.access_token_expired:
    gauth.Refresh()
    gauth.SaveCredentialsFile("mycreds.txt")
else:
    gauth.Authorize()

drive = GoogleDrive(gauth)


def sign_up(email, password):
    try:
        # Create user using Firebase Admin SDK
        user = auth.create_user(email=email, password=password)
        print("User created successfully!")
        return user
    except Exception as e:
        print("Error:", e)
        return None


def sign_in(email, password):
    try:
        # Firebase Admin doesn't directly support sign-in, so you'll have to implement token verification or use Firebase Authentication SDK
        # For the purpose of this example, Firebase Admin only supports server-side functions (no direct sign-in).
        print("Signed in successfully!")
        return True
    except Exception as e:
        print("Error:", e)
        return None


def create_csv(user_email):
    filename = user_email.replace("@", "_").replace(".", "_") + ".csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Data"])
    print(f"CSV file {filename} created.")
    return filename


def upload_csv(filename):
    file = drive.CreateFile({'title': filename})
    file.SetContentFile(filename)
    file.Upload()
    print("File uploaded successfully.")
    return file['id']


def edit_csv(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    print("Data added successfully.")


if __name__ == "__main__":
    email = input("Enter email: ")
    password = input("Enter password: ")
    action = input("Sign Up (S) or Sign In (I)? ").strip().lower()

    user = None
    if action == 's':
        user = sign_up(email, password)
    elif action == 'i':
        user = sign_in(email, password)

    if user:
        csv_file = create_csv(email)
        edit_csv(csv_file, [1, "Sample Data"])
        file_id = upload_csv(csv_file)
        print("File ID:", file_id)
