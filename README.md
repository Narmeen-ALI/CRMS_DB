
# Crime Report Management System (CRMS)

A web-based application built with **Flask** to manage criminal records, evidence, and official reports. This system provides a streamlined interface for law enforcement to track suspects, manage case files, and generate official PDF documentation.

## Project Structure

Based on the repository files, the system is organized as follows:

* **app.py**: The core Flask application containing backend logic and routing.
* **generate_pdf.py**: A specialized script for generating downloadable PDF reports.
* **database.sql**: The database schema used to initialize the system's storage.
* **requirements.txt**: List of Python dependencies needed to run the app.
* **Frontend Templates**:
* index.html & home.html`: Main landing and dashboard pages.
* records.html & suspects.html`: Interfaces for managing criminal data.
* evidence.html: Module for tracking case evidence.
* report.html: Interface for filing new crime reports.
* map.html: Geospatial visualization of crime data/locations.


* **Assets**: `style.css`, `script.js`, and `justice.jpg`.

##  Tech Stack

* **Backend:** Python (Flask)
* **Database:** SQL (Standard Relational Database)
* **PDF Generation:** Python PDF libraries (via `generate_pdf.py`)
* **Frontend:** HTML5, CSS3, JavaScript
.

##  Key Features

* **Centralized Record Management:** Manage suspects and criminal history in one place.
* **Digital FIR Filing:** Submit and store crime reports digitally.
* **Evidence Tracking:** Maintain logs of physical and digital evidence.
* **Automated PDF Generation:** Generate official case documents using the built-in PDF tool.
* **Crime Mapping:** Visualize crime data points on a map.
