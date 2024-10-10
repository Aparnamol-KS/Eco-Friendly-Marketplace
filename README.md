# Eco-Friendly-Marketplace

## Project Overview
The **Eco-Friendly Marketplace** is a Django-based web application where users can browse and purchase eco-friendly products. The platform emphasizes sustainability by showcasing products with various eco-certifications, and includes features like a product wishlist, shopping cart, and eco-certification page.


---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Setup](#setup)
5. [Running the Application](#running-the-application)


---

## Technologies Used
- **Django**: Web framework for building the backend and templates
- **SQLite**: Default database for development (can be changed for production)
- **HTML/CSS**: Frontend technologies for the user interface
- **Git/GitHub**: Version control and collaboration

---


## Setup
### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/username/eco-friendly-marketplace.git
cd eco-friendly-marketplace
```

### 2. Set up a Virtual Environment
```bash
python -m venv env
```
### 3. Activate the virtual environment
```bash
env\Scripts\activate
```
### 4. Install Dependencies
Make sure you have all necessary Python packages installed by running this command
```bash
pip install -r requirements.txt
```
### 5. Migrate the database 
After setting up the environment, run the migrations to set up the database
```bash
python manage.py migrate
```
---

## Running the Application
### Start the Development Server 
Once everything is set up, you can run the server with
```bash 
python manage.py runserver
```
















