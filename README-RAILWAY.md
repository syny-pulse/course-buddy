# How to Deploy Course Buddy on Railway

You're all set up with the necessary configuration files for Railway! I've added a few files to your project to make deployment smooth:
- `requirements.txt`: Tells Railway's build system which Python packages to install, including `gunicorn`, an industrial-grade web server.
- `Procfile` & `railway.toml`: Deployment configs that tell Railway exactly how to start your app.
- `.gitignore`: Ensures you don't accidentally push the `instance/coursework.db` SQLite file or your `venv/` to GitHub.

Here is the step-by-step guide to get your application live.

## Step 1: Push Your Code to GitHub

Railway deploys applications automatically by connecting directly to your GitHub repository.

1. Open your terminal in the `d:\course-buddy` folder.
2. Initialize Git if you haven't already:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with Railway configs"
   ```
3. Go to [GitHub](https://github.com/) and create a new repository (name it something like `course-buddy`).
4. Copy the repository URL and add the remote to your local directory:
   ```bash
   git remote add origin https://github.com/your-username/course-buddy.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Create a Railway Account

1. Go to [Railway.app](https://railway.app/).
2. Click **Login** and sign in using your **GitHub** account so Railway can access your repositories.

## Step 3: Deploy the App

1. In the Railway dashboard, click **+ New Project** (or **Create a New Project**).
2. Select **Deploy from GitHub repo**.
3. Railway might ask you to configure the GitHub app to give it access to your repositories. Grant it access to your `course-buddy` repository.
4. Select the `course-buddy` repository from the list.
5. Railway will immediately start building your application using the files we created. 
6. Wait for the build phase to complete. It will automatically detect Python, install `requirements.txt`, and start the app using `gunicorn` (defined in the `Procfile`).

## Step 4: Expose to the Internet

Once the build is complete, you need to generate a public URL for your application.

1. Click on your newly deployed service in the Railway dashboard.
2. Go to the **Settings** tab.
3. Scroll down to the **Networking** section.
4. Under **Public Networking**, click **Generate Domain**.
5. Railway will give you a free `.up.railway.app` URL. Click on it to see your live Course Buddy!

> [!IMPORTANT]  
> **A Note on SQLite Data Persistence**
> 
> Railway's standard compute instances are ephemeral, meaning that every time you deploy a new version of your code, the disk resets. Because Course Buddy uses a local SQLite database (`coursework.db`), **your data might be lost between deployments**.
>
> **To fix this, you must attach a Volume:**
> 1. In your Railway service settings, go to the **Volumes** tab.
> 2. Click **Add Volume**.
> 3. Provide a mount path. Important: You must change your app's database URI to use a path exactly matching this mount point. For example, if you mount it at `/data`, you'll need to change `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/coursework.db'`.
>
> Alternatively, you could spin up a PostgreSQL database in Railway and swap out your SQLite connection string for the provided `DATABASE_URL`!
