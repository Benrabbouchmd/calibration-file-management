# Calibration File Management 📊

=====================================

## Overview 🤔

---

This project is a Flask-based web application that allows users to read and store calibration files (CFs) in a database. The application provides an API for querying the content of the CFs and retrieving specific key-value pairs.

### Features 🎉

- Read and store CFs in a database 📁
- Query the content of CFs using a RESTful API 📊
- Retrieve specific key-value pairs from CFs 🔍

## Getting Started 🚀

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/Benrabbouchmd/calibration-file-management.git

```

### Step 2: Build and Run the Docker Container

```bash
docker build -t cf_mgmt .
docker run -d -p 5000:5000 cf_mgmt
```

## API Endpoints 📚

### Read and Store CFs

- **Endpoint:** `/api/calibration/store`
- **Method:** POST
- **Description:** Read and store CFs in the database

### Query the Content of CFs

- **Endpoint:** `/api/calibration/content`
- **Method:** GET
- **Description:** Query the content of CFs
- **Query Parameters:**
  - `query` (string): The key or parameter to search for in the CFs content.

### Get All CFs

- **Endpoint:** `/api/calibration`
- **Method:** GET
- **Description:** Get all CFs in the database
- **Query Parameters:**
  - `search` (string): Optional search term to filter CFs.
  - `id` (integer): Optional ID to specify a particular CF to read and store.

## Database Schema 📈

| Column            | Type       | Constraints                                              | Description                               |
| ----------------- | ---------- | -------------------------------------------------------- | ----------------------------------------- |
| `id`              | Integer    | Primary Key                                              | Unique identifier for each CF entry       |
| `pandora_id`      | String     |                                                          | Identifier for the Pandora instrument     |
| `spectrometer_id` | String     |                                                          | Identifier for the spectrometer           |
| `version`         | String     |                                                          | Version of the calibration file           |
| `validity_date`   | String     |                                                          | Validity starting date (YYYYMMDD format)  |
| `content`         | Text       |                                                          | Content of the calibration file           |
| `created_at`      | Integer    | Default: Current timestamp                               | Timestamp when the entry was created      |
| `updated_at`      | Integer    | Default: Current timestamp, on update: Current timestamp | Timestamp when the entry was last updated |
| `file_hash`       | String(32) | Unique                                                   | MD5 hash of the file for uniqueness       |
